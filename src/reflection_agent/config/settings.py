"""
Application settings backed by Pydantic BaseSettings.

Reads from environment variables (and .env) with full validation,
type coercion, and sensible defaults.  One source of truth for every
runtime knob.
"""

from enum import StrEnum
from functools import lru_cache

from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings


class Provider(StrEnum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"


class Settings(BaseSettings):
    """Validated, immutable application configuration."""

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8", "extra": "ignore"}

    # --- Provider selection ---
    model_provider: Provider = Field(
        default=Provider.OPENAI,
        description="Which LLM provider to use",
    )
    reflection_max_messages: int = Field(
        default=6,
        ge=2,
        description="Max messages in state before the reflection loop ends",
    )

    # --- OpenAI ---
    openai_api_key: SecretStr = Field(default=SecretStr(""), description="OpenAI API key")
    openai_model: str = Field(default="gpt-4o", description="OpenAI model name")
    openai_temperature: float = Field(default=0.7, ge=0.0, le=2.0)

    # --- Anthropic (ready for future use) ---
    anthropic_api_key: SecretStr = Field(default=SecretStr(""), description="Anthropic API key")
    anthropic_model: str = Field(
        default="claude-3-5-sonnet-20241022",
        description="Anthropic model name",
    )
    anthropic_temperature: float = Field(default=0.7, ge=0.0, le=1.0)

    # --- LangSmith / Observability ---
    langchain_api_key: str = Field(default="", description="LangSmith API key")
    langchain_tracing_v2: bool = Field(default=False)
    langchain_project: str = Field(default="reflection-agent")

    # --- Application ---
    log_level: str = Field(default="INFO")
    environment: str = Field(default="development")

    @field_validator("log_level")
    @classmethod
    def _normalise_log_level(cls, v: str) -> str:
        return v.upper()


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Singleton-cached settings instance."""
    return Settings()
