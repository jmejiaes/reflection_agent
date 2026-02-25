"""
Strategy pattern for LLM providers.
Each strategy knows its env vars, defaults, and how to build the chat model.
Adding a provider = implement a strategy and register it.
"""

from functools import lru_cache
import os
from typing import Protocol

from langchain_core.language_models import BaseChatModel

from config.settings import Provider


class LLMProviderStrategy(Protocol):
    """Contract for LLM provider strategies.

    Strategies implementing this protocol must be able to build
    a BaseChatModel instance using parameters and configuration
    relevant to their provider (model, API key, temperature, etc).

    Implementing this method allows swapping providers
    without changing the rest of the code.
    """

    # Add Env vars and default values

    def build_llm(self) -> BaseChatModel:
        ...


class OpenAIStrategy:
    ENV_MODEL = "OPENAI_MODEL"
    ENV_TEMPERATURE = "OPENAI_TEMPERATURE"
    ENV_API_KEY = "OPENAI_API_KEY"

    DEFAULT_MODEL = "gpt-4o"
    DEFAULT_TEMPERATURE = 0.7

    def build_llm(self) -> BaseChatModel:
        from langchain_openai import ChatOpenAI

        model = os.getenv(self.ENV_MODEL, self.DEFAULT_MODEL)
        temperature = float(
            os.getenv(self.ENV_TEMPERATURE, str(self.DEFAULT_TEMPERATURE))
        )
        api_key = os.getenv(self.ENV_API_KEY)
        return ChatOpenAI(model=model, temperature=temperature, api_key=api_key)


# class AnthropicStrategy:
#     ENV_MODEL = "ANTHROPIC_MODEL"
#     ENV_TEMPERATURE = "ANTHROPIC_TEMPERATURE"
#     ENV_API_KEY = "ANTHROPIC_API_KEY"

#     DEFAULT_MODEL = "claude-3-5-sonnet-20241022"
#     DEFAULT_TEMPERATURE = 0.7
#     def build_llm(self) -> BaseChatModel: ...


_STRATEGIES: dict[Provider, LLMProviderStrategy] = {
    Provider.openai: OpenAIStrategy(),
    # Provider.anthropic: AnthropicStrategy(),
}


@lru_cache(maxsize=4)
def get_llm(provider: Provider) -> BaseChatModel:
    if provider not in _STRATEGIES:
        raise ValueError(f"Provider has no registered strategy: {provider}")
    return _STRATEGIES[provider].build_llm()