"""
LCEL chain factories (prompt | llm).

Each factory accepts an explicit LLM so chains are easy to test with stubs.
Falls back to the application-default LLM when none is provided.
"""

from __future__ import annotations

from langchain_core.language_models import BaseChatModel
from langchain_core.runnables import RunnableSerializable

from reflection_agent.config.llm_strategies import get_llm
from reflection_agent.graph.prompts import generation_prompt, reflection_prompt


def get_generation_chain(llm: BaseChatModel | None = None) -> RunnableSerializable:
    return generation_prompt | (llm or get_llm())


def get_reflection_chain(llm: BaseChatModel | None = None) -> RunnableSerializable:
    return reflection_prompt | (llm or get_llm())
