from enum import Enum
from pprint import pformat

import decimal
import logging
import datetime
from typing import Iterable, Set, Tuple

from pydantic import BaseModel

from plant_species.models import Species
from species_data.enrichment.config import EnrichmentConfig
from species_data.enrichment.models import ConfidenceModel, get_species_data_model
from species_data.enrichment.utils import get_fields
from species_data.models import (
    Source,
    SourceType,
)
from species_data.models.models import SpeciesProperties
from .chains import get_enrichment_chain
from .exceptions import NoValuesSetException

logger = logging.getLogger(__name__)


def set_decimalrange_property(
    species_properties: SpeciesProperties,
    prop_name: str,
    prop_value: dict,
    sources: Iterable[Source],
):
    """Sets a decimal range property on a SpeciesProperties instance."""

    logger.debug(
        f"Setting {prop_name} on {species_properties.species}. Value: {prop_value}"
    )

    for value_name in ["minimum", "typical", "maximum", "confidence"]:
        value = getattr(prop_value, value_name, None)
        if value:
            # Doing decimal.Decimal directly (on floats) gives really eff'ed up rounding errors!
            # So we need to go str first. The decimal conversion is just bonus.
            decimal_value = decimal.Decimal(str(value))
            # logger.debug(
            #     f"Setting decimal value: {decimal_value} for input {value} on {prop_name}_{value_name}"
            # )
            setattr(
                species_properties,
                f"{prop_name}_{value_name}",
                decimal_value,
            )
        else:
            logger.info(f"No value for {prop_name}_{value_name}, skipping")

    sources_attr = getattr(species_properties, f"{prop_name}_sources")
    sources_attr.set(sources)


def set_category_property(
    species_properties: SpeciesProperties,
    prop_name: str,
    prop_value: ConfidenceModel,
    sources: Iterable[Source],
):
    """Sets a category property on a SpeciesProperties instance."""

    if not getattr(prop_value, "values", None):
        logger.info("No values in {prop_name}, skipping.")
        return

    logger.debug(f"Setting {prop_name} with {prop_value}")

    values: Set[Enum] = prop_value.values  # type: ignore
    for value in values:
        # Derive category_class, the other side of the M2M)
        # and through_class (what links them) them
        # using prop_name on species_properties.
        # Both category_class and through_class are Django models,
        # as is SpeciesProperties.
        prop = getattr(species_properties, prop_name)  # ManyRelatedManager

        category_class = prop.model
        through_class = prop.through

        # Sometimes value is empty!?
        if value:
            get_values = {
                "species": species_properties,
            }

            try:
                get_values[prop.target_field_name] = category_class.objects.get(
                    slug=value.value
                )
            except category_class.DoesNotExist:
                print(f"Warning! {prop_name} with slug {value} not found!")
                continue

            try:
                obj = through_class.objects.get(**get_values)
            except through_class.DoesNotExist:
                obj = through_class(**get_values)

            obj.confidence = prop_value.confidence
            obj.full_clean()
            obj.save()

            obj.sources.set(sources)


def enrich_species_data(species: Species, config: EnrichmentConfig):
    """Retrieves and stores additional data about a plant species using a language model."""

    data_model = get_species_data_model()
    chain = get_enrichment_chain(config, data_model)

    # if not species.wikipedia_page:
    #     logger.warning(f"No Wikipedia page for {species}, skipping.")
    #     return

    # Brute force token limit.
    # source_content = species.wikipedia_page.content[:25000]

    # assert source_content

    plant_data: BaseModel
    citations: Iterable[str]

    plant_data, citations = chain.invoke(
        {
            # "source_content": source_content,
            "species_name": str(species),
        }
    )

    logger.debug(f"Received data: {pformat(plant_data)}")

    source_type = SourceType.objects.get_or_create(name="Perplexity")[0]

    sources = []
    for url in citations:
        source = Source.objects.get_or_create(
            url=url,
            source_type=source_type,
            defaults={
                "date": datetime.datetime.now(),
            },
        )[0]

        sources.append(source)

    species_properties = SpeciesProperties.objects.get_or_create(species=species)[0]

    fields = get_fields(SpeciesProperties)
    assert fields
    assert len(fields.decimalranges) > 0
    assert len(fields.categories) > 0

    for prop_name, prop_value in [
        (prop_name, getattr(plant_data, prop_name))
        for prop_name in fields.decimalranges
    ]:
        if prop_value:
            # TODO: Only update when confidence is higher!
            set_decimalrange_property(
                species_properties, prop_name, prop_value, sources
            )

    species_properties.full_clean()

    species_properties.save()
    logger.debug(f"Saved {species_properties}")

    # For each of EcologicalRole, GrowthHabit, HumanUse and Climate zone:
    # when given, lookup category based on slug in values and update species with it,
    # storing CategorizedSpeciesPropertyThroughBase and get_or_create'ing a Source with SourceType named Wikipedi
    # with the URL of the Wikipedia page.

    for prop_name, prop_value in [
        (prop_name, getattr(plant_data, prop_name)) for prop_name in fields.categories
    ]:
        if prop_value:
            set_category_property(species_properties, prop_name, prop_value, sources)

    # Prevent completely empty data. We can only test this after it has been created due to the
    # relational map. It precludes things like empty Wikipedia pages.
    if not any(
        [
            getattr(species_properties, f"{field}_{value}")
            for field in fields.decimalranges
            for value in ["minimum", "typical", "maximum"]
        ]
    ) and not any(
        [getattr(species_properties, field).exists() for field in fields.categories]
    ):
        # Reverse save.
        species_properties.delete()
        raise NoValuesSetException(f"Deleted {species_properties}: no values set.")
