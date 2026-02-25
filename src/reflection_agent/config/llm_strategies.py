"""
Strategy pattern for LLM provider construction.

Each strategy encapsulates provider-specific details (SDK import, params).
The registry maps Provider → Strategy and is the single place to extend
when adding a new backend.
"""

from __future__ import annotations

import logging
from typing import Protocol

from langchain_core.language_models import BaseChatModel

from reflection_agent.config.settings import Provider, Settings, get_settings
from reflection_agent.exceptions import (
    LLMInvocationError,
    ProviderNotRegisteredError,
)

logger = logging.getLogger(__name__)


class LLMStrategy(Protocol):
    """Contract every LLM provider strategy must satisfy."""

    def build_llm(self, settings: Settings) -> BaseChatModel: ...


class OpenAIStrategy:
    """Builds a ChatOpenAI instance from application settings."""

    def build_llm(self, settings: Settings) -> BaseChatModel:
        from langchain_openai import ChatOpenAI

        try:
            return ChatOpenAI(
                model=settings.openai_model,
                temperature=settings.openai_temperature,
                api_key=settings.openai_api_key,
            )
        except Exception as exc:
            raise LLMInvocationError(provider="openai", cause=exc) from exc


class AnthropicStrategy:
    """Builds a ChatAnthropic instance from application settings."""

    def build_llm(self, settings: Settings) -> BaseChatModel:
        from langchain_anthropic import ChatAnthropic

        try:
            return ChatAnthropic(
                model_name=settings.anthropic_model,
                temperature=settings.anthropic_temperature,
                api_key=settings.anthropic_api_key,
                timeout=None,
                stop=None,
            )
        except Exception as exc:
            raise LLMInvocationError(provider="anthropic", cause=exc) from exc


_STRATEGY_REGISTRY: dict[Provider, LLMStrategy] = {
    Provider.OPENAI: OpenAIStrategy(),
    Provider.ANTHROPIC: AnthropicStrategy(),
}


def get_llm(provider: Provider | None = None, settings: Settings | None = None) -> BaseChatModel:
    """
    Resolve the LLM for the given (or default) provider.

    Accepts explicit settings for testability; falls back to the cached singleton.
    """
    settings = settings or get_settings()
    provider = provider or settings.model_provider

    strategy = _STRATEGY_REGISTRY.get(provider)
    if strategy is None:
        raise ProviderNotRegisteredError(provider.value)

    logger.info("Building LLM", extra={"provider": provider.value})
    return strategy.build_llm(settings)
