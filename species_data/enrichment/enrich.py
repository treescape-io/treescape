import logging
import decimal
import datetime
from langchain_core.language_models import BaseLLM

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


def enrich_species_data(species: Species, llm: BaseLLM):
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

    (source_type, created) = SourceType.objects.get_or_create(name="Wikipedia")
    (source, created) = Source.objects.get_or_create(
        name=species.wikipedia_page.title,
        source_type=source_type,
        url=f"https://en.wikipedia.org/w/index.php?title={species.wikipedia_page.title}&oldid={species.wikipedia_page.revision_id}",
        date=datetime.datetime.now(),
    )

    (species_properties, created) = SpeciesProperties.objects.get_or_create(
        species=species
    )

    range_properties = ["height", "width"]
    for prop in range_properties:
        # TODO: Only update when confidence is higher!
        if prop in plant_data:
            plant_prop = plant_data[prop]

            logger.info(
                f"Setting {prop} on {species_properties.species}. Data: {plant_prop}"
            )

            # if plant_prop["minimum"]:
            #     setattr(
            #         species_properties,
            #         f"{prop}_minimum",
            #         decimal.Decimal(plant_prop["minimum"]),
            #     )
            # if plant_prop["typical"]:
            #     setattr(
            #         species_properties,
            #         f"{prop}_typical",
            #         decimal.Decimal(plant_prop["typical"]),
            #     )
            if plant_prop["maximum"]:
                setattr(
                    species_properties,
                    f"{prop}_maximum",
                    decimal.Decimal(plant_prop["maximum"]),
                )

            if plant_prop["confidence"]:
                setattr(
                    species_properties, f"{prop}_confidence", plant_prop["confidence"]
                )

            setattr(species_properties, f"{prop}_source", source)

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

    for category_name, category_class, through_class in categories:
        if category_name in plant_data:
            category_data = plant_data[category_name]

            for value in category_data["values"]:
                # Sometimes value is empty!?
                if value:
                    props = {
                        "species": species_properties,
                        "source": source,
                        "confidence": category_data["confidence"],
                    }

                    try:
                        props[category_name] = category_class.objects.get(slug=value)
                    except category_class.DoesNotExist:
                        print(f"Warning! {category_name} with slug {value} not found!")
                        continue

                    (obj, created) = through_class.objects.update_or_create(**props)
