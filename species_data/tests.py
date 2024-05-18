from django.test import TestCase
from unittest.mock import Mock
from langchain_community.llms.fake import FakeListLLM
from species_data.enrichment.enrich import enrich_species_data
from plant_species.models import Species


class EnrichSpeciesDataTest(TestCase):
    def test_enrich_species_data(self):
        responses = [
            '{"action": "Python REPL", "action_input": "print(2 + 2)"}',
            '{"final_answer": 4}',
        ]
        llm = FakeListLLM(responses=responses)

        mock_species = Mock(spec=Species)
        mock_species.wikipedia_page.content = "Sample content"
        mock_species.latin_name = "Sample Latin Name"

        enrich_species_data(mock_species, llm)

        # Add assertions here based on expected behavior
        # For example, you might want to check if certain methods were called on the mock_species object
        # or if certain attributes were set.
