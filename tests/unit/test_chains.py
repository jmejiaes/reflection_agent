"""Tests for graph.chains module — uses FakeLLM to avoid network calls."""

from __future__ import annotations

from langchain_core.messages import HumanMessage

from reflection_agent.graph.chains import get_generation_chain, get_reflection_chain


class TestChainConstruction:
    def test_generation_chain_returns_runnable(self, fake_llm):
        chain = get_generation_chain(llm=fake_llm)
        assert callable(getattr(chain, "invoke", None))

    def test_reflection_chain_returns_runnable(self, fake_llm):
        chain = get_reflection_chain(llm=fake_llm)
        assert callable(getattr(chain, "invoke", None))


class TestChainInvocation:
    def test_generation_chain_produces_output(self, fake_llm):
        chain = get_generation_chain(llm=fake_llm)
        result = chain.invoke({"messages": [HumanMessage(content="Hello")]})
        assert result.content == fake_llm.response_text

    def test_reflection_chain_produces_output(self, fake_llm):
        chain = get_reflection_chain(llm=fake_llm)
        result = chain.invoke({"messages": [HumanMessage(content="Hello")]})
        assert result.content == fake_llm.response_text
