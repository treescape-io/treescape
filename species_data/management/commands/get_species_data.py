import pprint
from typing import Optional
import dspy

from dspy.functional import TypedPredictor

from django.core.management.base import BaseCommand, CommandError
from pydantic import BaseModel

from plant_species.models import Species
from species_data.models import GrowthHabit
from species_data.models.categories import ClimateZone, EcologicalRole, HumanUse

from species_data.enrichment.models import SpeciesData


class SpeciesOption(BaseModel):
    name: str


class SpeciesOptions(BaseModel):
    growth_habits: Optional[list[SpeciesOption]]
    # climate_zones: Optional[list[SpeciesOption]]
    human_uses: Optional[list[SpeciesOption]]
    ecological_role: Optional[list[SpeciesOption]]


class SpeciesDataPredictor(dspy.Signature):
    """Generate species data based on provided context."""

    context: dspy.Optional[str] = dspy.InputField(
        desc="When available, should be considered the source of truth for species data."
    )
    latin_name: str = dspy.InputField(
        desc="Latin name of the species to return data for."
    )
    options: SpeciesOptions = dspy.InputField(
        desc="Available options for fields with limited options."
    )
    species_data: SpeciesData = dspy.OutputField(
        desc="Data about species. Optional fields for which no data is available should remain empty."
    )


def get_options_for(model) -> list[SpeciesOption]:
    return [SpeciesOption(name=option.name) for option in model.objects.all()]


def get_species_options() -> SpeciesOptions:
    return SpeciesOptions(
        growth_habits=get_options_for(GrowthHabit),
        # climate_zones=get_options_for(ClimateZone),
        human_uses=get_options_for(HumanUse),
        ecological_role=get_options_for(EcologicalRole),
    )


def get_species_data():
    gpt3_instruct = dspy.OpenAI(model="gpt-3.5-turbo-instruct")
    dspy.configure(lm=gpt3_instruct)
    generator = TypedPredictor(SpeciesDataPredictor)

    for species in Species.objects.all():
        print(f"Getting data for: {species}")
        options = get_species_options()
        output = generator(
            latin_name=species.latin_name,
            context=species.wikipedia_page.content,
            options=options,
        )
        pprint.pprint(gpt3_instruct.inspect_history(n=1))
        assert "species_data" in output
        pprint.pprint(dict(output.species_data))


class Command(BaseCommand):
    help = "Populates the database with species data."

    def handle(self, *args, **options):
        try:
            get_species_data()
        except Exception as e:
            # Catch and re-raise any exceptions.
            raise CommandError(e)

        self.stdout.write(
            self.style.SUCCESS(
                f"WOEI"
                # f"Successfully added {add_count} new species out of {len(species_list)} in the list, skipped {synonym_count} synonyms"
            )
        )
