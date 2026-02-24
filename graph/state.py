"""
Estado del grafo y constantes de nodos.
Centralizar aquí permite evolucionar el state y el naming en un solo lugar (LLMOps).
"""

from typing import Annotated, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class MessageGraph(TypedDict):
    """Estado que cada nodo del grafo lee y actualiza."""

    messages: Annotated[list[BaseMessage], add_messages]


# Nombres de nodos (usados en edges y conditional_edges)
REFLECT = "reflect"
GENERATE = "generate"
