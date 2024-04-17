import pprint

from tqdm import tqdm

from django.core.management.base import BaseCommand, CommandError

from langchain_openai import OpenAI
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate

from plant_species.models import Species

from species_data.enrichment.models import get_species_data_model


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

    SpeciesData = get_species_data_model()
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

    # TODO:
    # 1. Auto-generated slugs for all multi-select models.
    # 2. Idempotently save generated data to models.
    # 3. Fixture/data migration for Source Type.
    # 4. Citations for source.
    # 5. Set source for created data.
    # 6. Dynamic prompting without source.
    # 7. Source type confidence.
    # 8. Add additional sources, confidence-based trumping:
    #     - a) USDA
    #     - b) GBIF description
    #     - c) Trefle
    #


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
