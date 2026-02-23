from ast import List
from email import message
from typing import TypedDict, Annotated

from dotenv import load_dotenv
from urllib3 import response

load_dotenv()

from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages

from graph.chains import reflect_chain, generate_chain


# State of the graph
# Es la estructura de datos que cada nodo del grafo va a acceder y actualizar
class MessageGraph(TypedDict):
    messages: Annotated[
        list[BaseMessage], add_messages
    ]  # Annotated sirve para añadir metadatos a un tipo sin cambiar el tipo en sí,
    # en este caso se está especificando que add messages será la manera en que se actualizará el state


# Constantes necesarias para el nombrado de los nodos
REFLECT = "reflect"
GENERATE = "generate"


def generation_node(state: MessageGraph):
    """Genera un nuevo mensaje con el chain de generación y actualiza el estado.

    Args:
        state: Estado actual del grafo (TypedDict con clave "messages").

    Returns:
        Dict con clave "messages" conteniendo una lista con el mensaje generado
        (list[BaseMessage]); que se fusiona con el estado existente vía add_messages.
    """
    current_messages = {"messages": state["messages"]}
    return {"messages": [generate_chain.invoke(current_messages)]}


def reflection_node(state: MessageGraph):
    """Genera un nuevo mensaje con el chain de generación y actualiza el estado.

    Args:
        state: Estado actual del grafo (TypedDict con clave "messages").

    Returns:
        Dict con clave "messages" conteniendo una lista con el mensaje generado
        (list[BaseMessage]); que se fusiona con el estado existente vía add_messages.
    """
    current_messages = {"messages": state["messages"]}
    reflection_chain_response = reflect_chain.invoke(current_messages)
    return {"messages": HumanMessage(content=reflection_chain_response.content)}
    # Notemos que este reflection node devuelve su respuesta como
    # un human message, esto es para que el otro agente crea que
    # es conversacional, es una Prompt Engeneering Technique


def main():

    ## -- Graph Definition --
    builder = StateGraph(state_schema=MessageGraph)
    builder.add_node(
        GENERATE, generation_node
    )  # Aquí se eestá como nombrando que se hará referencia al nodo de generacion con el STR de GENERATE
    builder.add_node(REFLECT, reflection_node)
    builder.set_entry_point(
        GENERATE
    )  # Aquí se define que este será el punto de entrada al grafo.
    # Que es analogo a un edge de START a el GENERATE.

    def should_continue(state: MessageGraph):
        """
        Esta funcion sera la condicional encargada de definir si seguir reflexionando, que puede a futuro
        ser un llm, o otra tecnica.
        Esto define el flow.
        """
        if len(state["messages"]) > 6:
            return END
        return REFLECT

    # builder.add_conditional_edges(GENERATE, should_continue) # Esto significa que cada que se genere, se quiere que se evalue la funcion de should continue.
    ## Lo que pasa es que si se pone así, esto deja no tan claro para Langgraph qué posibles destinations nodes tiene GENERATE.
    builder.add_conditional_edges(
        GENERATE, should_continue, path_map={END: END, REFLECT: REFLECT}
    )
    builder.add_edge(REFLECT, GENERATE)

    # Final Graph instantiatiion
    graph = (
        builder.compile()
    )  # 'The compiled graph implements the Runnable interface and can be invoked, streamed, batched, and run asynchronously.'
    print(
        graph.get_graph().draw_mermaid()
    )  # returns a mermaid representatio of the compiled graph.


if __name__ == "__main__":
    main()
