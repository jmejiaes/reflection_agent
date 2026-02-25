"""Shared fixtures for the test suite."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage

from reflection_agent.config.settings import Settings


@pytest.fixture()
def test_settings(monkeypatch: pytest.MonkeyPatch) -> Settings:
    """Return a Settings instance with safe defaults (no real API keys)."""
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("MODEL_PROVIDER", "openai")
    monkeypatch.setenv("REFLECTION_MAX_MESSAGES", "4")
    monkeypatch.setenv("ENVIRONMENT", "testing")
    return Settings()


class FakeLLM(BaseChatModel):
    """Deterministic stub for unit tests — no network calls."""

    response_text: str = "Fake LLM response"

    @property
    def _llm_type(self) -> str:
        return "fake"

    def _generate(self, messages: list[BaseMessage], **kwargs) -> MagicMock:
        from langchain_core.outputs import ChatGeneration, ChatResult

        msg = AIMessage(content=self.response_text)
        return ChatResult(generations=[ChatGeneration(message=msg)])


@pytest.fixture()
def fake_llm() -> FakeLLM:
    return FakeLLM(response_text="This is a great tweet! #Python #AI")
