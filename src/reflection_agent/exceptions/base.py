"""
Exception hierarchy.

All domain exceptions inherit from ReflectionAgentError so callers can
catch a single base class when they don't need fine-grained handling.
"""


class ReflectionAgentError(Exception):
    """Root exception for every error raised by this package."""


class ConfigurationError(ReflectionAgentError):
    """Invalid or missing configuration (env vars, settings file, etc.)."""


class ProviderError(ReflectionAgentError):
    """Base for LLM-provider related failures."""


class ProviderNotRegisteredError(ProviderError):
    """Requested provider has no registered strategy."""

    def __init__(self, provider: str) -> None:
        super().__init__(f"No strategy registered for provider '{provider}'")
        self.provider = provider


class LLMInvocationError(ProviderError):
    """The LLM call itself failed (timeout, rate-limit, bad response, …)."""

    def __init__(self, provider: str, cause: Exception) -> None:
        super().__init__(f"LLM invocation failed for provider '{provider}': {cause}")
        self.provider = provider
        self.__cause__ = cause


class GraphExecutionError(ReflectionAgentError):
    """A graph node or the orchestration logic failed."""
