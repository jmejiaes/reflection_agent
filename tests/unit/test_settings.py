"""Tests for config.settings module."""

from __future__ import annotations

import pytest

from reflection_agent.config.settings import Provider, Settings


class TestProvider:
    def test_valid_providers(self):
        assert Provider("openai") == Provider.OPENAI
        assert Provider("anthropic") == Provider.ANTHROPIC

    def test_invalid_provider_raises(self):
        with pytest.raises(ValueError):
            Provider("nonexistent")


class TestSettings:
    def test_defaults(self, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.delenv("MODEL_PROVIDER", raising=False)
        monkeypatch.delenv("REFLECTION_MAX_MESSAGES", raising=False)
        s = Settings()
        assert s.model_provider == Provider.OPENAI
        assert s.reflection_max_messages == 6
        assert s.openai_model == "gpt-4o"

    def test_env_override(self, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.setenv("MODEL_PROVIDER", "anthropic")
        monkeypatch.setenv("REFLECTION_MAX_MESSAGES", "10")
        monkeypatch.setenv("OPENAI_MODEL", "gpt-3.5-turbo")
        s = Settings()
        assert s.model_provider == Provider.ANTHROPIC
        assert s.reflection_max_messages == 10
        assert s.openai_model == "gpt-3.5-turbo"

    def test_log_level_normalised(self, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.setenv("LOG_LEVEL", "debug")
        s = Settings()
        assert s.log_level == "DEBUG"

    def test_invalid_max_messages(self, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.setenv("REFLECTION_MAX_MESSAGES", "1")
        with pytest.raises(ValueError):
            Settings()

    def test_temperature_range(self, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.setenv("OPENAI_TEMPERATURE", "3.0")
        with pytest.raises(ValueError):
            Settings()
