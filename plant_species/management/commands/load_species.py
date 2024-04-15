from tqdm import tqdm
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from ...exceptions import SpeciesAlreadyExists
from ...models import Species

# Path to species_list.txt, getting current directory where script resides.
species_txt = Path(__file__).resolve().parent / "species_list.txt"


class Command(BaseCommand):
    help = "Idempotent loading of species data."

    def handle(self, *args, **options):
        # Iterate over species_list.txt in local directory
        try:
            with open(species_txt, "r") as species_file:
                species_list = species_file.readlines()

            species_list = [s.strip() for s in species_list]

            add_count = 0
            synonym_count = 0
            for species_name in tqdm(species_list):
                try:
                    # Check literal name
                    Species.objects.get(latin_name=species_name)
                except Species.DoesNotExist:
                    s = Species(latin_name=species_name)
                    try:
                        s.enrich_data()
                    except SpeciesAlreadyExists:
                        # Skip synonyms
                        synonym_count += 1
                        continue

                    s.full_clean()
                    s.save()
                    add_count += 1
        except Exception as e:
            # Catch and re-raise any exceptions.
            raise CommandError(e)

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully added {add_count} new species out of {len(species_list)} in the list, skipped {synonym_count} synonyms"
            )
        )
