from langchain.globals import set_verbose, set_debug
from langchain_core.language_models import BaseLanguageModel
from langchain.output_parsers import (
    PydanticOutputParser,
    OutputFixingParser,
    RetryOutputParser,
)
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda, RunnableParallel
from langchain_openai import ChatOpenAI


from .models import get_species_data_model

# set_verbose(True)
# set_debug(True)


def get_enrichment_chain():
    """Generates a chain for enriching plant species data using a language model."""

    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.1,
        model_kwargs={"response_format": {"type": "json_object"}},
        max_tokens=512,  # Increases available tokens for input.
    )

    fallback_llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0.1,
        model_kwargs={"response_format": {"type": "json_object"}},
        max_tokens=512,  # Increases available tokens for input.
    )

    prompt_template = """As a plant expert, return available information about the plant species '{latin_name}'.

    Base your answers exclusively on the following source:

    Source:
    ```
    {source_content}
    ```

    Important guidelines:
    - Requested properties are optional, return `null` for a property if no relevant information is available in the source.
    - When minimum, maximum or typical values are not specified, return `null`. Never guess a value!
    - Specify length units in meters.
    - Return at most 1 decimal for numbers.
    - Width concerns the canopy width of a plant, not the trunk.
    - Only when setting a property, include your level of confidence in the values for a property, based on the source data.
    - For categorical properties, only select your answer from provided values.
    - If a property has no value, no confidence is required.

    {format_instructions}

    Example output:
    ```
    {example}
    ```

    Avoid this:
    ```
    {{
        "height": {{
            "confidence": null,
            "minimum": null,
            "typical": null,
            "maximum": null
        }}
    }}
    ```
    Instead, do this:
    ```
    {{
        'height': null
    }}
    ```
    """

    example = """{"ecological_roles": {"confidence": 0.9,
                          "values": ["carbon-sequestration",
                                     "habitat-provision",
                                     "nitrogen-fixation",
                                     "pest-and"]},
     "growth_habits": {"confidence": 0.8, "values": ["tree"]},
     "height": {"confidence": 0.9, "maximum": 30, "minimum": 15, "typical": 30},
     "human_uses": {"confidence": 0.9,
                    "values": ["animal-fodder",
                               "firewood",
                               "fiber",
                               "timber",
                               "medicinal-bark",
                               "medicinal-flowers",
                               "medicinal-leaves",
                               "medicinal-roots",
                               "ornamental-bark",
                               "ornamental-flowers",
                               "ornamental-foliage"],},
     "width": null,
     "propagation_methods": null
    }"""
    SpeciesData = get_species_data_model()

    parser = PydanticOutputParser(pydantic_object=SpeciesData)
    parser = OutputFixingParser.from_llm(parser=parser, llm=llm, max_retries=3)
    parser = OutputFixingParser.from_llm(parser=parser, llm=fallback_llm, max_retries=1)

    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["latin_name", "source_content"],
        partial_variables={
            "format_instructions": parser.get_format_instructions(),
            "example": example,
        },
    )

    chain = prompt | llm | parser

    return chain
