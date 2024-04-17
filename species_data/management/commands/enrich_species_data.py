from tqdm import tqdm

from django.core.management.base import BaseCommand, CommandError

from species_data.enrichment.enrich import enrich_species_data
from plant_species.models import Species


class Command(BaseCommand):
    """Django management command to enrich plant species data using a language model."""

    help = "Generates additional data about plant species using a language model."

    def handle(self, *args, **options):
        try:
            species_list = Species.objects.all()[:5]

            with tqdm(species_list) as pbar:
                for species in pbar:
                    pbar.set_description(f"Processing {species}")
                    enrich_species_data(species)

        except Exception as e:
            # Catch and re-raise any exceptions.
            raise CommandError(e)

        self.stdout.write(self.style.SUCCESS("Successfully generated species data."))
