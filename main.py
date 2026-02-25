"""
Entry point: compiles the graph, prints Mermaid and invokes.
"""

from dotenv import load_dotenv

load_dotenv()

from langchain_core.messages import HumanMessage

from graph import build_graph


def main() -> None:
    graph = build_graph()
    # Graph visualization (useful for documentation and debugging)
    print(graph.get_graph().draw_mermaid())

    # Example: invoke with an initial message (uncomment to test)
    QUERY = "Make this tweet better: @me, 'Python is awesome, and langraph, nothing is like it'"
    result = graph.invoke({"messages": [HumanMessage(content=QUERY)]})
    print(result["messages"][-1].content)


if __name__ == "__main__":
    main()
