"""
CLI entry-point for the reflection agent.

Keeps main.py thin: parse args, configure logging, run the graph.
"""

from __future__ import annotations

import argparse

from langchain_core.messages import HumanMessage

from reflection_agent.config import get_settings
from reflection_agent.graph import build_graph
from reflection_agent.logging import setup_logging


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse CLI args. If argv is None, argparse uses sys.argv (normal execution)."""
    parser = argparse.ArgumentParser(
        prog="reflection-agent",
        description="Generate and iteratively refine a tweet via an LLM reflection loop.",
    )
    parser.add_argument(
        "query",
        nargs="?",
        default="Write a viral tweet about how Python and LangGraph are changing AI development",
        help="Initial prompt / tweet request (default: demo prompt)",
    )
    parser.add_argument(
        "--mermaid",
        action="store_true",
        help="Print the Mermaid graph diagram and exit",
    )
    # parse_args(None) → argparse uses sys.argv[1:]; pass a list for tests.
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    settings = get_settings()
    setup_logging(log_level=settings.log_level, environment=settings.environment)

    args = _parse_args(argv)
    graph = build_graph()

    if args.mermaid:
        print(graph.get_graph().draw_mermaid())
        return

    result = graph.invoke({"messages": [HumanMessage(content=args.query)]})
    final = result["messages"][-1].content
    print("\n" + final)


if __name__ == "__main__":
    main()
