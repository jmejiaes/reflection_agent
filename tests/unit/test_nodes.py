"""Tests for graph.nodes — uses monkeypatch to inject FakeLLM chains."""

from __future__ import annotations

from unittest.mock import patch

from langchain_core.messages import HumanMessage

from reflection_agent.graph.chains import get_generation_chain, get_reflection_chain
from reflection_agent.graph.nodes import generation_node, reflection_node


class TestGenerationNode:
    def test_returns_messages_key(self, fake_llm):
        state = {"messages": [HumanMessage(content="Write a tweet")]}
        chain = get_generation_chain(llm=fake_llm)
        with patch(
            "reflection_agent.graph.nodes.get_generation_chain",
            return_value=chain,
        ):
            result = generation_node(state)

        assert "messages" in result
        assert len(result["messages"]) == 1

    def test_output_is_string_content(self, fake_llm):
        state = {"messages": [HumanMessage(content="Write a tweet")]}
        chain = get_generation_chain(llm=fake_llm)
        with patch(
            "reflection_agent.graph.nodes.get_generation_chain",
            return_value=chain,
        ):
            result = generation_node(state)

        assert isinstance(result["messages"][0], str)


class TestReflectionNode:
    def test_returns_human_message(self, fake_llm):
        state = {"messages": [HumanMessage(content="Draft tweet")]}
        chain = get_reflection_chain(llm=fake_llm)
        with patch(
            "reflection_agent.graph.nodes.get_reflection_chain",
            return_value=chain,
        ):
            result = reflection_node(state)

        msg = result["messages"][0]
        assert isinstance(msg, HumanMessage)
