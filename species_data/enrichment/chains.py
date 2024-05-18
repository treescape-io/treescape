from langchain_core.language_models import BaseLLM
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate


from .models import get_species_data_model


def get_enrichment_chain(llm: BaseLLM):
    """Generates a chain for enriching plant species data using a language model."""

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

    chain = prompt | llm | output_parser

    return chain
