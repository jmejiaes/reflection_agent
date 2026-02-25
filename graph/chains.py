"""
LCEL chains (prompt | llm) per node.
The LLM is obtained from the active provider's strategy (Strategy pattern).
"""

from langchain_core.language_models import BaseChatModel

from config.llm_strategies import get_llm
from config.settings import get_model_provider
from graph.prompts import generation_prompt, reflection_prompt


def _get_llm() -> BaseChatModel:
    """
    Centralizes default LLM resolution.

    Provides a single place to define how the language model used by default
    in the chains is resolved.
    """
    return get_llm(get_model_provider())


def get_generate_chain():
    return generation_prompt | _get_llm()


def get_reflect_chain():
    return reflection_prompt | _get_llm()
