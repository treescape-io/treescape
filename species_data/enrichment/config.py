from dataclasses import dataclass

from langchain_core.language_models import BaseLanguageModel
from langchain_openai.chat_models import ChatOpenAI


@dataclass
class EnrichmentConfig:
    llm: BaseLanguageModel
    fallback_llm: BaseLanguageModel


def get_default_config():
    return EnrichmentConfig(
        llm=ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.3,
            model_kwargs={"response_format": {"type": "json_object"}},
            max_tokens=512,  # Increases available tokens for input.
        ),
        fallback_llm=ChatOpenAI(
            model="gpt-4o",
            temperature=0.1,
            model_kwargs={"response_format": {"type": "json_object"}},
            max_tokens=512,  # Increases available tokens for input.
        ),
    )
