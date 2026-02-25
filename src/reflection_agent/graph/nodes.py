"""
Graph nodes.

Each node is a plain function with signature (state) → dict and is
responsible for one atomic step in the reflection loop.
"""

from __future__ import annotations

import logging

from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.runnables import RunnableSerializable

from reflection_agent.exceptions import GraphExecutionError
from reflection_agent.graph.chains import get_generation_chain, get_reflection_chain
from reflection_agent.graph.state import AgentState

logger = logging.getLogger(__name__)


def _invoke_chain(chain: RunnableSerializable, state: AgentState, node: str) -> BaseMessage:  # type: ignore[type-arg]
    """Invoke a chain and translate provider errors into domain exceptions."""
    try:
        result: BaseMessage = chain.invoke({"messages": state["messages"]})
        return result
    except Exception as exc:
        logger.exception("Chain invocation failed", extra={"node": node})
        raise GraphExecutionError(f"Node '{node}' failed: {exc}") from exc


def generation_node(state: AgentState) -> dict:
    """Produce (or revise) a tweet based on the conversation so far."""
    logger.info("Generating tweet", extra={"msg_count": len(state["messages"])})
    response = _invoke_chain(get_generation_chain(), state, "generate")
    return {"messages": [response.content]}


def reflection_node(state: AgentState) -> dict:
    """Critique the latest generation and return feedback as a HumanMessage."""
    logger.info("Reflecting on tweet", extra={"msg_count": len(state["messages"])})
    response = _invoke_chain(get_reflection_chain(), state, "reflect")
    return {"messages": [HumanMessage(content=response.content)]}
