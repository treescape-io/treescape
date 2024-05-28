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

        # Allow comments in species list.
        species_list = [
            s.strip() for s in species_list if not s.lstrip().startswith("#")
        ]

        add_count = 0
        synonym_count = 0

        with tqdm(species_list) as pbar:
            for species_name in pbar:
                if not Species.objects.filter(latin_name=species_name).exists():
                    pbar.write(f"Adding '{species_name}'.")

                    species = Species(latin_name=species_name)

                    # Do this before full_clean to properly capture SpeciesAlreadyExists.
                    try:
                        species.full_clean()
                    except ValidationError as e:
                        if isinstance(e.__cause__, SpeciesAlreadyExists) or any(
                            # In some cases, we have several ValidationError's, like show:
                            # django.core.exceptions.ValidationError: {
                            #   'genus': ['This field cannot be null.'],
                            #   '__all__': ["Species 'Acacia nilotica' already  exists under name 'Vachellia nilotica'."],
                            #   'gbif_id': ['Species with this GBIF usageKey already exists.']
                            # }
                            [
                                isinstance(e[0].__cause__, SpeciesAlreadyExists)
                                for e in e.error_dict.values()
                            ]
                        ):
                            synonym_count += 1
                            pbar.write(f"Skipping synonym species: '{species_name}'.")
                            continue

                        # Unexpected exception, re-raise.
                        raise Exception(
                            f"ValidationError for {species_name}: {str(e)}"
                        ) from e

                    species.save()
                    species.enrich_related()

                    add_count += 1
                else:
                    pbar.write(f"Skipping existing species: {species_name}.")

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully added {add_count} new species out of {len(species_list)} in the list, skipped {synonym_count} synonyms"
            )
        )
