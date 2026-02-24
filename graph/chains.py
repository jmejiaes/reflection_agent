"""
Cadenas LCEL (prompt | llm) por nodo.
El LLM se obtiene de la estrategia del proveedor activo (patrón Strategy).
"""

from langchain_core.language_models import BaseChatModel

from config.llm_strategies import get_llm
from config.settings import get_model_provider
from graph.prompts import generation_prompt, reflection_prompt


def _get_llm() -> BaseChatModel:
    """
    Centraliza la obtención del LLM por defecto.

    Proporciona un único punto donde definir cómo se resuelve el modelo de lenguaje que
    se usará por defecto en los chains.
    """
    return get_llm(get_model_provider())


def get_generate_chain():
    return generation_prompt | _get_llm()


def get_reflect_chain():
    return reflection_prompt | _get_llm()
