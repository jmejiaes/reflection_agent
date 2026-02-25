"""Tests for the exception hierarchy."""

from reflection_agent.exceptions import (
    ConfigurationError,
    GraphExecutionError,
    LLMInvocationError,
    ProviderNotRegisteredError,
    ReflectionAgentError,
)


class TestExceptionHierarchy:
    def test_all_inherit_from_base(self):
        for exc_cls in (
            ConfigurationError,
            GraphExecutionError,
            LLMInvocationError,
            ProviderNotRegisteredError,
        ):
            assert issubclass(exc_cls, ReflectionAgentError)

    def test_provider_not_registered_message(self):
        exc = ProviderNotRegisteredError("fake-provider")
        assert "fake-provider" in str(exc)
        assert exc.provider == "fake-provider"

    def test_llm_invocation_wraps_cause(self):
        cause = RuntimeError("timeout")
        exc = LLMInvocationError(provider="openai", cause=cause)
        assert exc.__cause__ is cause
        assert "openai" in str(exc)
