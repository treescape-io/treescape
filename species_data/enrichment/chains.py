import json
import logging
from typing import Type
from langchain.globals import set_verbose, set_debug
from langchain.output_parsers import (
    PydanticOutputParser,
    RetryWithErrorOutputParser,
)
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda, RunnableParallel
from pydantic.v1 import BaseModel

from species_data.enrichment.config import EnrichmentConfig


logger = logging.getLogger(__name__)

set_verbose(True)
# set_debug(True)

# Here to save whitespace in input.
_prompt_template = """As a plant data entry expert, return available information about the plant species '{latin_name}' who strictly follows the provided JSON schema.

Base your answers exclusively on the following source:

Source:
```
{source_content}
```

Important guidelines:
- Requested properties are optional, leave them out in your reply if no relevant information is available in the source.
- Specify length units in meters.
- Return at most 2 decimals for numeric properties.
- The value of `maximum` should always be higher than `typical` and `minimum` should be lower still.
- If only the `maximum` and or `minimum` are specified in the source, leave `typical` out.
- The value of `width` concerns the canopy width of a plant, not the trunk.
- When returning a value for a property, include you `confidence`, based on the source data.
- If no information is available for a property, leave the property out and do not return `confidence` for that property.
- For categorical properties (like `ecological_roles`, `climate_zones`, `human_uses` and others) , only return values allowed in the schema's enum. Other values are rejected.
- For categorical properties, if none of the values are relevant, find the closest one from the schema or leave the value out.
- Never return invalid `values`, the parsing will fail and we'll have to start again.

Example output:
```
{example}
```
Another example
```
{example2}
```

{format_instructions}
"""


def get_enrichment_chain(config: EnrichmentConfig, data_model: Type[BaseModel]):
    """Generates a chain for enriching plant species data using a language model."""

    example = json.dumps(
        {
            "ecological_roles": {
                "confidence": 0.8,
                "values": [
                    "carbon-sequestration",
                    "habitat-provision",
                    "soil-erosion-control",
                    "shade-provision",
                ],
            },
            "growth_habits": {"confidence": 1, "values": ["tree"]},
            "height": {"confidence": 0.9, "maximum": 30, "minimum": 15, "typical": 30},
            "human_uses": {
                "confidence": 0.9,
                "values": [
                    "animal-fodder",
                    "firewood",
                    "fiber",
                    "timber",
                    "medicinal-bark",
                    "medicinal-flowers",
                    "medicinal-leaves",
                    "medicinal-roots",
                    "ornamental-bark",
                    "ornamental-flowers",
                    "ornamental-foliage",
                ],
            },
        }
    )

    example2 = json.dumps(
        {
            "growth_habits": {"confidence": 1, "values": ["tree"]},
            "climate_zones": {
                "confidence": 1,
                "values": [
                    "tropical-rainforest-climate",
                    "tropical-monsoon-climate",
                    "tropical-wet-and-dry-or-savanna-climate-dry-summer",
                    "tropical-wet-and-dry-or-savanna-climate-dry-winter",
                ],
            },
            "ecological_roles": {
                "confidence": 0.8,
                "values": [
                    "carbon-sequestration",
                    "habitat-provision",
                    "soil-erosion-control",
                    "shade-provision",
                ],
            },
            "soil_preferences": {"confidence": 0.9, "values": ["clayey", "sandy"]},
        }
    )
    parser = PydanticOutputParser(pydantic_object=data_model)

    retry_parser = RetryWithErrorOutputParser.from_llm(parser=parser, llm=config.llm)

    prompt = PromptTemplate(
        template=_prompt_template,
        input_variables=["latin_name", "source_content"],
        partial_variables={
            "format_instructions": parser.get_format_instructions(),
            "example": example,
            "example2": example2,
        },
    )

    completion_chain = prompt | config.llm

    main_chain = RunnableParallel(
        completion=completion_chain, prompt_value=prompt
    ) | RunnableLambda(
        lambda response: retry_parser.parse_with_prompt(
            completion=response["completion"].content,
            prompt_value=response["prompt_value"],
        )
    )

    return main_chain.with_retry(stop_after_attempt=3)
