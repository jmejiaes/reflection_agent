"""Tests for config.llm_strategies module."""

from __future__ import annotations

import pytest

from reflection_agent.config.llm_strategies import _STRATEGY_REGISTRY, get_llm
from reflection_agent.config.settings import Provider
from reflection_agent.exceptions import ProviderNotRegisteredError


class TestStrategyRegistry:
    def test_openai_registered(self):
        assert Provider.OPENAI in _STRATEGY_REGISTRY

    def test_anthropic_registered(self):
        assert Provider.ANTHROPIC in _STRATEGY_REGISTRY


class TestGetLLM:
    def test_unknown_provider_raises(self, test_settings, monkeypatch):
        monkeypatch.setattr("reflection_agent.config.llm_strategies._STRATEGY_REGISTRY", {})
        with pytest.raises(ProviderNotRegisteredError):
            get_llm(provider=Provider.OPENAI, settings=test_settings)
