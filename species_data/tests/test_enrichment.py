import decimal
from django.test import TestCase
from langchain_core.language_models import FakeListChatModel
from species_data.enrichment.config import EnrichmentConfig
from species_data.enrichment.enrich import enrich_species_data
from plant_species.models import Species, Genus, Family
from species_data.enrichment.models import get_species_data_model
from species_data.models.categories import (
    ClimateZone,
    EcologicalRole,
    GrowthHabit,
    HumanUse,
    SoilPreference,
)
from species_data.models.models import SpeciesProperties


def _get_species():
    # TODO: Proper mocks, not requiring internet access.
    family = Family.objects.create(latin_name="Family", gbif_id=34343)
    genus = Genus.objects.create(latin_name="Genus", gbif_id=3435123, family=family)

    species = Species.objects.create(
        latin_name="Quercus robur", gbif_id=34343, genus=genus
    )

    return species


class EnrichSpeciesDataTest(TestCase):
    def test_enrich_species_data(self):
        ResponseModel = get_species_data_model()

        response_data = {
            "growth_habits": {"confidence": 1, "values": ["tree"]},
            "climate_zones": {
                "confidence": 1,
                "values": [
                    "tropical-rainforest-climate",
                    "tropical-monsoon-climate",
                    "tropical-wet-and-dry-or-savanna-climate-dry-summer",
                    "tropical-wet-and-dry-or-savanna-climate-dry-winter",
                ],
            },
            "human_uses": {
                "confidence": 1.0,
                "values": ["fiber", "timber", "medicinal-bark", "dye"],
            },
            "ecological_roles": {
                "confidence": 0.8,
                "values": [
                    "carbon-sequestration",
                    "habitat-provision",
                    "soil-erosion-control",
                    "shade-provision",
                ],
            },
            "soil_preferences": {"confidence": 0.9, "values": ["clayey", "sandy"]},
            "height": {
                "confidence": 0.1,
                "minimum": 25,
                "typical": 32.5,
                "maximum": 40,
            },
        }

        response_obj = ResponseModel.parse_obj(response_data)

        # response = ChatMessage(role="AI", content=)

        # print(pformat(response_json))
        config = EnrichmentConfig(
            llm=FakeListChatModel(responses=[response_obj.json()]),
            fallback_llm=FakeListChatModel(responses=[response_obj.json()]),
        )

        species = _get_species()

        enrich_species_data(species, config)

        # Get species_data corresponding to species
        properties: SpeciesProperties = species.properties  # pyright: ignore reportAttributeAccessIssue

        self.assertTrue(properties)
        self.assertQuerysetEqual(
            properties.growth_habits.all(), GrowthHabit.objects.filter(slug="tree")
        )
        self.assertQuerysetEqual(
            properties.climate_zones.all(),
            ClimateZone.objects.filter(
                slug__in=[
                    "tropical-rainforest-climate",
                    "tropical-monsoon-climate",
                    "tropical-wet-and-dry-or-savanna-climate-dry-summer",
                    "tropical-wet-and-dry-or-savanna-climate-dry-winter",
                ]
            ),
        )
        self.assertQuerysetEqual(
            properties.human_uses.all(),
            HumanUse.objects.filter(
                slug__in=["fiber", "timber", "medicinal-bark", "dye"]
            ),
        )
        self.assertQuerysetEqual(
            properties.ecological_roles.all(),
            EcologicalRole.objects.filter(
                slug__in=[
                    "carbon-sequestration",
                    "habitat-provision",
                    "soil-erosion-control",
                    "shade-provision",
                ]
            ),
        )
        self.assertQuerysetEqual(
            properties.soil_preferences.all(),
            SoilPreference.objects.filter(slug__in=["clayey", "sandy"]),
        )
        # Test source and confidence on Through
        self.assertTrue(properties.speciesgrowthhabit_set.first().source)  # pyright: ignore reportAttributeAccessIssue
        self.assertTrue(properties.speciesclimatezone_set.first().source)  # pyright: ignore reportAttributeAccessIssue
        self.assertTrue(properties.specieshumanuse_set.first().source)  # pyright: ignore reportAttributeAccessIssue
        self.assertTrue(properties.speciesecologicalrole_set.first().source)  # pyright: ignore reportAttributeAccessIssue
        self.assertTrue(properties.speciessoilpreference_set.first().source)  # pyright: ignore reportAttributeAccessIssue

        self.assertEqual(
            properties.speciesgrowthhabit_set.first().confidence,  # pyright: ignore reportAttributeAccessIssue
            decimal.Decimal("1"),
        )
        self.assertEqual(
            properties.speciesclimatezone_set.first().confidence,  # pyright: ignore reportAttributeAccessIssue
            decimal.Decimal("1"),
        )
        self.assertEqual(
            properties.specieshumanuse_set.first().confidence,  # pyright: ignore reportAttributeAccessIssue
            decimal.Decimal("1"),
        )
        self.assertEqual(
            properties.speciesecologicalrole_set.first().confidence,  # pyright: ignore reportAttributeAccessIssue
            decimal.Decimal("0.8"),
        )
        self.assertEqual(
            properties.speciessoilpreference_set.first().confidence,  # pyright: ignore reportAttributeAccessIssue
            decimal.Decimal("0.9"),
        )

        self.assertEqual(properties.height.minimum, decimal.Decimal("25"))
        self.assertEqual(properties.height.typical, decimal.Decimal("32.5"))
        self.assertEqual(properties.height.maximum, decimal.Decimal("40"))
        self.assertEqual(properties.height.confidence, decimal.Decimal("0.1"))
        self.assertTrue(properties.height.source)
