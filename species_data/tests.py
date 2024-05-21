from django.test import TestCase
from langchain_community.llms.fake import FakeListLLM
from species_data.enrichment.enrich import enrich_species_data
from plant_species.models import Species, Genus, Family


def get_species():
    # TODO: Proper mocks, not requiring internet access.
    family = Family.objects.create(latin_name="Family", gbif_id=34343)
    genus = Genus.objects.create(latin_name="Genus", gbif_id=3435123, family=family)

    species = Species.objects.create(
        latin_name="Quercus robur", gbif_id=34343, genus=genus
    )

    return species


class EnrichSpeciesDataTest(TestCase):
    def test_enrich_species_data(self):
        responses = [
            '{"action": "Python REPL", "action_input": "print(2 + 2)"}',
            '{"final_answer": 4}',
        ]
        llm = FakeListLLM(responses=responses)

        species = get_species()

        enrich_species_data(species, llm)

        # Add assertions here based on expected behavior
        # For example, you might want to check if certain methods were called on the mock_species object
        # or if certain attributes were set.
