from pprint import pformat

import decimal
import logging
import datetime
from langchain_core.language_models import BaseLanguageModel

from plant_species.models import Species
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
    plant_data: dict,
    prop_name: str,
    source: Source,
):
    """Sets a decimal range property on a SpeciesProperties instance."""

    plant_prop = plant_data[prop_name]

    logger.debug(
        f"Setting {prop_name} on {species_properties.species}. Data: {plant_prop}"
    )

    for value_name in ["minimum", "typical", "maximum", "confidence"]:
        value = plant_prop.get(value_name, None)
        if value:
            # Doing decimal.Decimal directly (on floats) gives really eff'ed up rounding errors!
            # So we need to go str first. The decimal conversion is just bonus.
            decimal_value = decimal.Decimal(str(value))
            logger.debug(
                f"Setting decimal value: {decimal_value} for input {value} on {prop_name}_{value_name}"
            )
            setattr(
                species_properties,
                f"{prop_name}_{value_name}",
                decimal_value,
            )
        else:
            logger.debug(f"{prop_name}_{value_name} was EMPTY")

    setattr(species_properties, f"{prop_name}_source", source)


def set_category_property(
    species_properties: SpeciesProperties,
    plant_data: dict,
    prop_name: str,
    source: Source,
):
    """Sets a category property on a SpeciesProperties instance."""

    if (
        prop_name not in plant_data
        or not plant_data[prop_name]
        or not plant_data[prop_name]["values"]
    ):
        return

    category_data = plant_data[prop_name]

    logger.debug(f"Setting {prop_name} with {category_data}")

    for value in category_data["values"]:
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
                    slug=value
                )
            except category_class.DoesNotExist:
                print(f"Warning! {prop_name} with slug {value} not found!")
                continue

            update_values = {
                "source": source,
                "confidence": category_data["confidence"],
            }

            through_class.objects.update_or_create(defaults=update_values, **get_values)
            # TODO: full_clean here (so explicit get/update)


def enrich_species_data(species: Species):
    """Retrieves and stores additional data about a plant species using a language model."""

    chain = get_enrichment_chain()

    if not species.wikipedia_page:
        logger.warning(f"No Wikipedia page for {species}, skipping.")
        return

    # Brute force token limit.
    source_content = species.wikipedia_page.content[:25000]

    assert source_content
    plant_data = chain.invoke(
        {
            "source_content": source_content,
            "latin_name": species.latin_name,
        }
    )

    logger.debug(f"Received data: {pformat(plant_data)}")

    source_type = SourceType.objects.get_or_create(name="Wikipedia")[0]
    source = Source.objects.get_or_create(
        url=f"https://en.wikipedia.org/w/index.php?title={species.wikipedia_page.title}&oldid={species.wikipedia_page.revision_id}",
        defaults={
            "name": species.wikipedia_page.title,
            "source_type": source_type,
            "date": datetime.datetime.now(),
        },
    )[0]

    species_properties = SpeciesProperties.objects.get_or_create(species=species)[0]

    fields = get_fields(SpeciesProperties)
    assert fields
    assert fields.decimalranges
    assert fields.categories

    for prop_name in fields.decimalranges:
        # TODO: Only update when confidence is higher!
        if prop_name in plant_data:
            set_decimalrange_property(species_properties, plant_data, prop_name, source)

    species_properties.full_clean()

    species_properties.save()
    logger.debug(f"Saved {species_properties}")

    # For each of EcologicalRole, GrowthHabit, HumanUse and Climate zone:
    # when given, lookup category based on slug in values and update species with it,
    # storing CategorizedSpeciesPropertyThroughBase and get_or_create'ing a Source with SourceType named Wikipedi
    # with the URL of the Wikipedia page.

    for prop_name in fields.categories:
        if prop_name in plant_data:
            set_category_property(species_properties, plant_data, prop_name, source)

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
