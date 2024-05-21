from django.forms import ValidationError
from tqdm import tqdm
from pathlib import Path

from django.core.management.base import BaseCommand

from plant_species.enrichment.exceptions import SpeciesAlreadyExists
from plant_species.models import Species

# Path to species_list.txt, getting current directory where script resides.
species_txt = Path(__file__).resolve().parent / "species_list.txt"


class Command(BaseCommand):
    help = "Idempotent loading of species data."

    def add_arguments(self, parser):
        parser.add_argument(
            "filename",
            nargs="?",
            type=str,
            default=str(species_txt),
            help="The file to load species from (default: species_list.txt)",
        )

    def handle(self, *args, **options):
        filename = options["filename"]
        # Iterate over species_list.txt in local directory
        with open(filename, "r") as species_file:
            species_list = species_file.readlines()

        species_list = [s.strip() for s in species_list]

        add_count = 0
        synonym_count = 0

        with tqdm(species_list) as pbar:
            for species_name in pbar:
                if not Species.objects.filter(latin_name=species_name).exists():
                    s = Species(latin_name=species_name)

                    # Do this before full_clean to properly capture SpeciesAlreadyExists.
                    try:
                        s.full_clean()
                    except ValidationError as e:
                        if isinstance(e.__cause__, SpeciesAlreadyExists):
                            synonym_count += 1
                            pbar.write(f"Skipping synonym species: {species_name}.")
                            continue

                    s.save()
                    s.enrich_related()

                    add_count += 1
                else:
                    pbar.write(f"Skipping existing species: {species_name}.")

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully added {add_count} new species out of {len(species_list)} in the list, skipped {synonym_count} synonyms"
            )
        )
