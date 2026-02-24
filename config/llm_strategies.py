"""
Patrón Strategy para proveedores de LLM.
Cada estrategia conoce sus variables de entorno, defaults y cómo construir el chat model.
Añadir un proveedor = implementar una estrategia y registrarla.
"""

from functools import lru_cache
import os
from typing import Protocol

from langchain_core.language_models import BaseChatModel

from config.settings import Provider


class LLMProviderStrategy(Protocol):
    """Contrato para estrategias de proveedor LLM.

    Las estrategias que implementen este protocolo deben poder construir
    una instancia de BaseChatModel usando los parámetros y configuración
    relevantes a su proveedor (modelo, API key, temperatura, etc).

    Implementar este método permite intercambiar entre proveedores
    sin cambiar el resto del código.
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
        raise ValueError(f"Proveedor sin estrategia registrada: {provider}")
    return _STRATEGIES[provider].build_llm()