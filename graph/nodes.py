"""
Nodos del grafo: generación y reflexión.
Cada nodo recibe el state y devuelve actualizaciones (dict con 'messages').
"""

from langchain_core.messages import HumanMessage
from langchain_core.runnables import Runnable

from graph.chains import get_generate_chain, get_reflect_chain
from graph.state import MessageGraph

def _messages_input(state: MessageGraph) -> dict:
    """Input que esperan los chains (prompt | llm): dict con 'messages'."""
    return {"messages": state["messages"]}

def _chain_invoke_with_messages(chain: Runnable, messages: dict):
    chain_response = chain.invoke(messages)
    return chain_response

def generation_node(state: MessageGraph) -> dict:
    """Genera un nuevo tweet con el chain de generación y actualiza el estado."""
    chain = get_generate_chain()
    current_messages = _messages_input(state)
    response = _chain_invoke_with_messages(current_messages)
    return {"messages": [response.content]}


def reflection_node(state: MessageGraph) -> dict:
    """Genera crítica/recomendaciones y las devuelve como HumanMessage (técnica de prompt)."""
    chain = get_reflect_chain()
    current_messages = _messages_input(state)
    response =  _chain_invoke_with_messages(current_messages)
    return {"messages": [HumanMessage(content=response.content)]}
