from langchain_core.language_models import BaseLanguageModel
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain.output_parsers import OutputFixingParser


from .models import get_species_data_model


def get_enrichment_chain(llm: BaseLanguageModel):
    """Generates a chain for enriching plant species data using a language model."""

    prompt_template = """As a plant expert, return available information about the plant species '{latin_name}'.

    Base your answers exclusively on the following source:

    Source:
    ```
    {source_content}
    ```

    Important guidelines:
    - Requested properties are optional, leave them out if no relevant information is provided in the source.
    - When minimum, maximum or typical values are not specified, return `null`. Never guess a value!
    - Specify length units in meters.
    - Return at most 1 decimal for numbers.
    - Width concerns the canopy width of a plant, not the trunk.
    - If and only if you return a property, include your level of confidence in the values for that property from the [0.0, 1.0] range.
    - For categorical properties, only select your answer from provided values.

    {format_instructions}
    """

    SpeciesData = get_species_data_model()

    json_parser = JsonOutputParser(pydantic_object=SpeciesData)
    fixing_parser = OutputFixingParser.from_llm(parser=json_parser, llm=llm)

    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["latin_name", "source_content"],
        partial_variables={
            "format_instructions": fixing_parser.get_format_instructions()
        },
    )

    chain = prompt | llm | fixing_parser

    return chain
