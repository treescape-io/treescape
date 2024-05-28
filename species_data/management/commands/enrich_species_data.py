from langchain_openai import ChatOpenAI
from tqdm import tqdm

from django.core.management.base import BaseCommand

from species_data.enrichment.enrich import enrich_species_data
from plant_species.models import Species


class Command(BaseCommand):
    """Django management command to enrich plant species data using a language model."""

    help = "Generates additional data about plant species using a language model."

    def handle(self, *args, **options):
        llm = ChatOpenAI(
            model="gpt-3.5-turbo-0125",
            temperature=0,
            model_kwargs={"response_format": {"type": "json_object"}},
            max_tokens=512,  # Increases available tokens for input.
        )

        species_list = Species.objects.filter(properties__isnull=True)

        with tqdm(species_list) as pbar:
            for species in pbar:
                pbar.set_description(f"Processing {species}")
                enrich_species_data(species, llm)

        self.stdout.write(self.style.SUCCESS("Successfully generated species data."))
