from tqdm import tqdm

from django.core.management.base import BaseCommand

from species_data.enrichment.config import get_default_config
from species_data.enrichment.enrich import enrich_species_data
from plant_species.models import Species
from species_data.enrichment.exceptions import NoValuesSetException


class Command(BaseCommand):
    """Django management command to enrich plant species data using a language model."""

    help = "Generates additional data about plant species using a language model."

    def handle(self, *args, **options):
        species_list = Species.objects.filter(properties__isnull=True)

        config = get_default_config()

        with tqdm(species_list) as pbar:
            for species in pbar:
                pbar.set_description(f"Processing {species}")

                try:
                    enrich_species_data(species, config)
                except NoValuesSetException as e:
                    pbar.write(f"Skipping no data: {species}: {e}")

        self.stdout.write(self.style.SUCCESS("Successfully generated species data."))
