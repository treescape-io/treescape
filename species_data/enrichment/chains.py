from langchain.globals import set_verbose, set_debug
from langchain_core.language_models import BaseLanguageModel
from langchain.output_parsers import PydanticOutputParser, OutputFixingParser
from langchain_core.prompts import PromptTemplate


from .models import get_species_data_model

set_verbose(True)
# set_debug(True)


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

    Example output:
    {example}
    """

    example = """{'ecological_roles': {'confidence': 0.9,
                          'values': ['carbon-sequestration',
                                     'habitat-provision',
                                     'nitrogen-fixation',
                                     'pest-and']},
     'growth_habits': {'confidence': 0.8, 'values': ['tree']},
     'height': {'confidence': 0.9, 'maximum': 30, 'minimum': 15, 'typical': 30},
     'human_uses': {'confidence': 0.9,
                    'values': ['animal-fodder',
                               'firewood',
                               'fiber',
                               'timber',
                               'medicinal-bark',
                               'medicinal-flowers',
                               'medicinal-leaves',
                               'medicinal-roots',
                               'ornamental-bark',
                               'ornamental-flowers',
                               'ornamental-foliage']}
    }"""

    SpeciesData = get_species_data_model()

    parser = PydanticOutputParser(pydantic_object=SpeciesData)
    parser = OutputFixingParser.from_llm(parser=parser, llm=llm, max_retries=3)

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
