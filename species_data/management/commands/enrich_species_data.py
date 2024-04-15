import decimal
import enum
import pprint

from typing import Optional

from tqdm import tqdm

from django.core.management.base import BaseCommand, CommandError
from django.utils.text import slugify

from langchain_openai import OpenAI
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field, create_model

from plant_species.models import Species
from species_data.models import GrowthHabit, HumanUse, EcologicalRole, ClimateZone


def get_model():
    """Generates a Pydantic model based on the Django models for plant species data categories."""

    class ConfidenceModel(BaseModel):
        confidence: decimal.Decimal = Field(gt=0, lt=1, decimal_places=1, max_digits=2)

    class DecimalRangeField(ConfidenceModel):
        minimum: Optional[decimal.Decimal] = Field(max_digit=3, decimal_places=1)
        typical: Optional[decimal.Decimal] = Field(max_digit=3, decimal_places=1)
        maximum: Optional[decimal.Decimal] = Field(max_digit=3, decimal_places=1)

    def generate_django_enum(model) -> enum.Enum:
        """Generates a string Enum based on the name field of MyModel instances."""
        # Retrieve all distinct name values from MyModel
        objects = model.objects.all()

        obj_dict = {slugify(obj): slugify(obj) for obj in objects}
        obj_enum = enum.Enum(f"{model.__name__}Enum", obj_dict)
        return obj_enum

    def generate_django_multiselect_field(model):
        """Generates a field allowing the selection of multiple options based on a given Django model."""
        model_enum = generate_django_enum(model)
        model = create_model(
            f"{model.__name__}Model",
            __base__=ConfidenceModel,
            values=(set[model_enum], ...),
        )

        return model

    class SpeciesData(BaseModel):
        height: DecimalRangeField = Field(description="mature plant height in meters")
        width: DecimalRangeField = Field(
            description="mature plant canopy diameter in meters"
        )

        growth_habits: generate_django_multiselect_field(GrowthHabit)
        human_uses: generate_django_multiselect_field(HumanUse)
        ecological_roles: generate_django_multiselect_field(EcologicalRole)
        climate_zones: generate_django_multiselect_field(ClimateZone)

    return SpeciesData


def get_llm_chain():
    """Generates a chain for enriching plant species data using a language model."""

    model = OpenAI(model="gpt-3.5-turbo-instruct", temperature=0)

    prompt_template = """As a plant expert, return available information about the plant species '{latin_name}'. Base your answers exclusively on the following source:

    Source:
    ```
    {source_content}
    ```

    Important: requested information is optional, do not return values for information not provided in the source.

    {format_instructions}
    """

    SpeciesData = get_model()
    output_parser = JsonOutputParser(pydantic_object=SpeciesData)

    format_instructions = output_parser.get_format_instructions()

    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["latin_name", "source_content"],
        partial_variables={"format_instructions": format_instructions},
    )

    chain = prompt | model | output_parser

    return chain


def enrich_species_data(species: Species):
    """Retrieves and stores additional data about a plant species using a language model."""
    chain = get_llm_chain()
    plant_data = chain.invoke(
        {
            "source_content": species.wikipedia_page.content,
            "latin_name": species.latin_name,
        }
    )
    pprint.pprint(plant_data)


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
