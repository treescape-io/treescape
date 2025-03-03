"""
This module contains fake chat models used for testing the species data enrichment functionality,
specially supporting structured output formats.
"""

from typing import Any, Dict, List, Type, Union
import json

from langchain_core.language_models import FakeListChatModel
from langchain_core.messages import BaseMessage
from pydantic import BaseModel
from langchain_core.runnables import (
    Runnable,
    RunnableBinding,
)


class FakeStructuredOutputChatModel(FakeListChatModel):
    """A fake chat model that supports structured output."""

    def with_structured_output(
        self,
        schema: Union[Dict[str, Any], Type[BaseModel], BaseModel],
        *,
        include_raw: bool = False,
        **kwargs: Any,
    ) -> Runnable[List[BaseMessage], Union[Dict[str, Any], BaseModel]]:
        """Creates a version of the model that outputs parsed structured objects.

        Args:
            schema: The schema to use for the structured outputs. Can be a Pydantic
                model, a dictionary schema, a dataclass, or a TypedDict.
            include_raw: If True, the raw LLM output will be included in the 
                output dictionary under the key "raw".
            **kwargs: Additional kwargs to pass to the structured output parser.

        Returns:
            A chain that takes in a list of BaseMessages and outputs an object matching
            the provided schema.
        """
        # For testing, we'll assume that the responses are already formatted
        # correctly according to the schema

        # Create a simple binding that will auto-add citations to the message
        def _handle_response(msgs: List[BaseMessage], **kwargs: Any) -> Dict[str, Any]:
            # Get the raw response from the model
            result = self.invoke(msgs)
            
            # Try to parse the response as JSON
            parsed = None
            if isinstance(schema, type) and issubclass(schema, BaseModel):
                try:
                    # Assume we received valid JSON from the model in the test
                    raw_json = json.loads(result.content)
                    # Parse it into the Pydantic model
                    parsed = schema.parse_obj(raw_json)
                except Exception:
                    # For testing purposes, we assume our fake responses are valid
                    # Try direct parsing as a fallback
                    try:
                        if hasattr(schema, "parse_obj"):
                            parsed = schema.parse_obj(json.loads(result.content))
                        else:
                            parsed = schema(**json.loads(result.content))
                    except Exception:
                        # Just use the raw JSON as fallback
                        parsed = json.loads(result.content)
            else:
                # Handle other schema types if needed
                parsed = result.content
                
            # Create the result object
            output = {"parsed": parsed}
            if include_raw:
                # For testing, we need to explicitly ensure citations are present
                if "additional_kwargs" not in result.__dict__:
                    result.additional_kwargs = {}
                if "citations" not in result.additional_kwargs:
                    result.additional_kwargs["citations"] = ["https://example.org/1", "https://example.org/2"]
                
                output["raw"] = result
                
            return output
            
        # Create a runnable binding that processes the messages
        chain = RunnableBinding(
            bound=self,
            kwargs={},
            config={},
            transform_input_fn=lambda x, **kwargs: x,
            transform_output_fn=_handle_response,
        )
        
        return chain