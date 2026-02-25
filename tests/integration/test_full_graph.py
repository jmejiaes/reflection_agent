"""
Integration test: runs the full graph with a FakeLLM.

Verifies the generate → reflect → generate loop terminates correctly.
"""

from __future__ import annotations

from unittest.mock import patch

from langchain_core.messages import HumanMessage

from reflection_agent.config.settings import Settings
from reflection_agent.graph.builder import build_graph
from tests.conftest import FakeLLM


def _make_settings() -> Settings:
    return Settings(
        openai_api_key="test",
        reflection_max_messages=4,
        environment="testing",
    )


class TestFullGraphExecution:
    def test_graph_terminates(self):
        fake = FakeLLM(response_text="Great tweet! #Python")
        settings = _make_settings()

        with (
            patch("reflection_agent.graph.chains.get_llm", return_value=fake),
            patch("reflection_agent.graph.builder.get_settings", return_value=settings),
        ):
            graph = build_graph()
            result = graph.invoke({"messages": [HumanMessage(content="Write a tweet about AI")]})

        assert len(result["messages"]) >= 2
        assert result["messages"][-1].content

    def test_final_message_has_content(self):
        fake = FakeLLM(response_text="AI is transforming everything")
        settings = _make_settings()

        with (
            patch("reflection_agent.graph.chains.get_llm", return_value=fake),
            patch("reflection_agent.graph.builder.get_settings", return_value=settings),
        ):
            graph = build_graph()
            result = graph.invoke({"messages": [HumanMessage(content="Tweet about LangGraph")]})

        final = result["messages"][-1].content
        assert isinstance(final, str)
        assert len(final) > 0
