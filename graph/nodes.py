"""
Graph nodes: generation and reflection.
Each node receives the state and returns updates (dict with 'messages').
"""

from langchain_core.messages import HumanMessage
from langchain_core.runnables import Runnable

from graph.chains import get_generate_chain, get_reflect_chain
from graph.state import MessageGraph

def _messages_input(state: MessageGraph) -> dict:
    """Input expected by chains (prompt | llm): dict with 'messages'."""
    return {"messages": state["messages"]}

def _chain_invoke_with_messages(chain: Runnable, messages: dict):
    chain_response = chain.invoke(messages)
    return chain_response

def generation_node(state: MessageGraph) -> dict:
    """Generates a new tweet with the generation chain and updates the state."""
    chain = get_generate_chain()
    current_messages = _messages_input(state)
    response = _chain_invoke_with_messages(current_messages)
    return {"messages": [response.content]}


def reflection_node(state: MessageGraph) -> dict:
    """Generates critique/recommendations and returns them as HumanMessage (prompt technique)."""
    chain = get_reflect_chain()
    current_messages = _messages_input(state)
    response =  _chain_invoke_with_messages(current_messages)
    return {"messages": [HumanMessage(content=response.content)]}
