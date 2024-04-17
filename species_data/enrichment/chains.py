from langchain_openai import OpenAI
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate


from .models import get_species_data_model


def get_enrichment_chain():
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


SpeciesEnrichmentChain = get_enrichment_chain()
