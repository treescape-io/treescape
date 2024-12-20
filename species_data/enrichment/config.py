from dataclasses import dataclass

from langchain_core.language_models import BaseLanguageModel

from langchain_openai.chat_models import ChatOpenAI
from langchain_community.chat_models.perplexity import ChatPerplexity
from django.conf import settings


@dataclass
class EnrichmentConfig:
    llm: BaseLanguageModel
    fallback_llm: BaseLanguageModel


def get_default_config():
    return EnrichmentConfig(
        llm=ChatPerplexity(
            api_key=settings.PPLX_API_KEY,
            model="llama-3.1-sonar-huge-128k-online",
            temperature=0.1,
            client=None,
            timeout=None,
        ),
        # llm=ChatOpenAI(
        #     model="gpt-4o-mini",
        #     temperature=0.1,
        #     model_kwargs={"response_format": {"type": "json_object"}},
        # ),
        fallback_llm=ChatOpenAI(
            model="gpt-4o",
            temperature=0.3,
            model_kwargs={"response_format": {"type": "json_object"}},
        ),
    )
