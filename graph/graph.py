"""
Construcción del grafo LangGraph.
Punto único donde se definen nodos, edges y conditional edges (LLMOps).
"""

from langgraph.graph import END, StateGraph

from config.settings import get_settings
from graph.nodes import generation_node, reflection_node
from graph.state import GENERATE, MessageGraph, REFLECT


def should_continue(state: MessageGraph):
    """Condición: seguir reflexionando o terminar según número de mensajes."""
    settings = get_settings()
    if len(state["messages"]) > settings.max_messages_before_end:
        return END
    return REFLECT


def build_graph() -> StateGraph:
    """Construye y compila el grafo de reflexión (generate → reflect → generate …)."""
    builder = StateGraph(state_schema=MessageGraph)
    builder.add_node(GENERATE, generation_node)
    builder.add_node(REFLECT, reflection_node)
    builder.set_entry_point(GENERATE)
    builder.add_conditional_edges(
        GENERATE, should_continue, path_map={END: END, REFLECT: REFLECT}
    )
    builder.add_edge(REFLECT, GENERATE)
    return builder.compile()
