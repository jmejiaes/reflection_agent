"""
Graph state and node constants.
Centralizing here allows evolving state and naming in one place (LLMOps).
"""

from typing import Annotated, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class MessageGraph(TypedDict):
    """State that each graph node reads and updates."""

    messages: Annotated[list[BaseMessage], add_messages]


# Node names (used in edges and conditional_edges)
REFLECT = "reflect"
GENERATE = "generate"
