"""
Graph state definition and node-name constants.

Single source of truth for the data contract between nodes and for node
identifiers used in edges / conditional edges.
"""

from enum import StrEnum
from typing import Annotated, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    """Immutable contract: every node receives and may update these keys."""

    messages: Annotated[list[BaseMessage], add_messages]


class NodeName(StrEnum):
    """Centralised node identifiers — avoids stringly-typed references."""

    GENERATE = "generate"
    REFLECT = "reflect"
