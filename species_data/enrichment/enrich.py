import logging
import datetime
from langchain_core.language_models import BaseLanguageModel

from plant_species.models import Species
from species_data.models import (
    Source,
    SourceType,
    EcologicalRole,
    GrowthHabit,
    HumanUse,
    ClimateZone,
)
from species_data.models.categories import (
    SpeciesClimateZone,
    SpeciesEcologicalRole,
    SpeciesGrowthHabit,
    SpeciesHumanUse,
)
from species_data.models.models import SpeciesProperties
from .chains import get_enrichment_chain

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

    property_list = ["minimum", "typical", "maximum", "confidence"]
    for property_name in property_list:
        setattr(
            species_properties,
            f"{prop_name}_{property_name}",
            plant_prop.get(property_name),
        )

    setattr(species_properties, f"{prop_name}_source", source)


def set_category_property(
    species_properties: SpeciesProperties,
    plant_data: dict,
    prop_name: str,
    source: Source,
):
    """Sets a category property on a SpeciesProperties instance."""
    category_data = plant_data[prop_name]

    for value in category_data["values"]:
        # Derive category_class, the other side of the M2M)
        # and through_class (what links them) them
        # using prop_name on species_properties.
        # Both category_class and through_class are Django models,
        # as is SpeciesProperties.
        category_class = getattr(species_properties, prop_name).related_model
        through_class = getattr(species_properties, prop_name).through

        # Sometimes value is empty!?
        if value:
            props = {
                "species": species_properties,
                "source": source,
                "confidence": category_data["confidence"],
            }

            try:
                props[prop_name] = category_class.objects.get(slug=value)
            except category_class.DoesNotExist:
                print(f"Warning! {prop_name} with slug {value} not found!")
                continue

            through_class.objects.update_or_create(**props)


def enrich_species_data(species: Species, llm: BaseLanguageModel):
    """Retrieves and stores additional data about a plant species using a language model."""

    chain = get_enrichment_chain(llm)

    assert species.wikipedia_page
    plant_data = chain.invoke(
        {
            "source_content": species.wikipedia_page.content,
            "latin_name": species.latin_name,
        }
    )

    # Plant data:
    # {'ecological_roles': {'confidence': 0.9,
    #                       'values': ['carbon-sequestration',
    #                                  'habitat-provision',
    #                                  'nitrogen-fixation',
    #                                  'pest-and']},
    #  'growth_habits': {'confidence': 0.8, 'values': ['tree']},
    #  'height': {'confidence': 0.9, 'maximum': 30, 'minimum': 15, 'typical': 30},
    #  'human_uses': {'confidence': 0.9,
    #                 'values': ['animal-fodder',
    #                            'firewood',
    #                            'fiber',
    #                            'timber',
    #                            'medicinal-bark',
    #                            'medicinal-flowers',
    #                            'medicinal-leaves',
    #                            'medicinal-roots',
    #                            'ornamental-bark',
    #                            'ornamental-flowers',
    #                            'ornamental-foliage']}

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

    range_properties = ["height", "width"]
    for prop_name in range_properties:
        # TODO: Only update when confidence is higher!
        if prop_name in plant_data:
            set_decimalrange_property(species_properties, plant_data, prop_name, source)

    species_properties.clean()
    species_properties.save()

    # For each of EcologicalRole, GrowthHabit, HumanUse and Climate zone:
    # when given, lookup category based on slug in values and update species with it,
    # storing CategorizedSpeciesPropertyThroughBase and get_or_create'ing a Source with SourceType named Wikipedi
    # with the URL of the Wikipedia page.

    categories = [
        ("ecological_role", EcologicalRole, SpeciesEcologicalRole),
        ("growth_habit", GrowthHabit, SpeciesGrowthHabit),
        ("human_use", HumanUse, SpeciesHumanUse),
        ("climate_zone", ClimateZone, SpeciesClimateZone),
    ]

    for prop_name, category_class, through_class in categories:
        if prop_name in plant_data:
            set_category_property(species_properties, plant_data, prop_name, source)
