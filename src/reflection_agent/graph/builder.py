"""
Graph construction — the wiring between nodes and edges.

Kept separate from node implementations so the topology can be visualised
or modified independently.
"""

from __future__ import annotations

import logging

from langgraph.graph import END, StateGraph
from langgraph.graph.state import CompiledStateGraph

from reflection_agent.config import get_settings
from reflection_agent.graph.nodes import generation_node, reflection_node
from reflection_agent.graph.state import AgentState, NodeName

logger = logging.getLogger(__name__)


def _should_continue(state: AgentState) -> str:
    """Route: keep reflecting or terminate based on message count."""
    settings = get_settings()
    if len(state["messages"]) >= settings.reflection_max_messages:
        return END
    return NodeName.REFLECT


def build_graph() -> CompiledStateGraph:
    """Assemble and compile the generate ⇄ reflect graph."""
    builder = StateGraph(state_schema=AgentState)

    builder.add_node(NodeName.GENERATE, generation_node)
    builder.add_node(NodeName.REFLECT, reflection_node)
    builder.set_entry_point(NodeName.GENERATE)

    builder.add_conditional_edges(
        NodeName.GENERATE,
        _should_continue,
        path_map={END: END, NodeName.REFLECT: NodeName.REFLECT},
    )
    builder.add_edge(NodeName.REFLECT, NodeName.GENERATE)

    logger.info("Graph compiled")
    return builder.compile()
