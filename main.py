"""
Punto de entrada: compila el grafo e imprime Mermaid e invoca.
"""

from dotenv import load_dotenv

load_dotenv()

from langchain_core.messages import HumanMessage

from graph import build_graph


def main() -> None:
    graph = build_graph()
    # Visualización del grafo (útil para documentación y debugging)
    print(graph.get_graph().draw_mermaid())

    # Ejemplo: invocar con un mensaje inicial (descomenta para probar)
    QUERY = "Make this tweet better: @me, 'Python is awesome, and langraph, nothing is like it'"
    result = graph.invoke({"messages": [HumanMessage(content=QUERY)]})
    print(result["messages"][-1].content)


if __name__ == "__main__":
    main()
