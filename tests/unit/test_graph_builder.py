"""Tests for graph.builder — verifies topology without invoking LLM."""

from __future__ import annotations

from unittest.mock import patch

from reflection_agent.graph.builder import _should_continue, build_graph
from reflection_agent.graph.state import AgentState, NodeName


class TestShouldContinue:
    def test_ends_when_max_messages_reached(self, test_settings):
        from langchain_core.messages import AIMessage, HumanMessage
        from langgraph.graph import END

        messages = [HumanMessage(content="hi"), AIMessage(content="hey")] * 3
        state: AgentState = {"messages": messages}

        with patch("reflection_agent.graph.builder.get_settings", return_value=test_settings):
            assert _should_continue(state) == END

    def test_continues_when_under_limit(self, test_settings):
        from langchain_core.messages import HumanMessage

        state: AgentState = {"messages": [HumanMessage(content="hi")]}
        with patch("reflection_agent.graph.builder.get_settings", return_value=test_settings):
            assert _should_continue(state) == NodeName.REFLECT


class TestBuildGraph:
    def test_graph_compiles(self):
        graph = build_graph()
        assert graph is not None

    def test_graph_has_mermaid(self):
        graph = build_graph()
        mermaid = graph.get_graph().draw_mermaid()
        assert "generate" in mermaid
        assert "reflect" in mermaid
