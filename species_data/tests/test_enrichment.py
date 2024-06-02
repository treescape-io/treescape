from pprint import pformat
from django.test import TestCase
from langchain_community.llms.fake import FakeListLLM
from species_data.enrichment.enrich import enrich_species_data
from plant_species.models import Species, Genus, Family
from species_data.enrichment.models import get_species_data_model


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
            "soil_preference": {"confidence": 0.9, "values": ["clayey", "sandy"]},
            "height": {
                "confidence": 0.1,
                "minimum": 25,
                "typical": 32.5,
                "maximum": 40,
            },
        }

        response = ResponseModel.parse_obj(response_data)

        # print(pformat(response_json))
        llm = FakeListLLM(responses=[response.json()])

        species = _get_species()

        enrich_species_data(species, llm)

        # Get species_data corresponding to species
        self.assertTrue(species.properties_id)
        species_data = species.properties
