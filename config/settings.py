"""
Configuration loaded from environment variables.
Makes it easy to change model, temperature and API keys without touching code (LLMOps).
"""

import os
from functools import lru_cache
from enum import Enum
from dotenv import load_dotenv

load_dotenv()

# Global env vars; provider-specific ones live in each strategy
ENV_MODEL_PROVIDER = "MODEL_PROVIDER"
ENV_REFLECTION_MAX_MESSAGES = "REFLECTION_MAX_MESSAGES"

DEFAULT_MODEL_PROVIDER = "openai"
DEFAULT_REFLECTION_MAX_MESSAGES = 3

class Provider(str, Enum):
    openai = "openai"
    anthropic = "anthropic"


# The @lru_cache(maxsize=1) decorator caches the result of the decorated function
# on first call and returns that same result on future calls.
# Thus get_settings() creates a Settings instance only once (simple singleton).
@lru_cache(maxsize=1)
def get_settings() -> "Settings":
    return Settings()


class Settings:
    """Agent (application) configuration.

    LLM-related settings (model, API key, ...) are resolved by the provider strategy.
    """

    max_messages_before_end: int

    def __init__(
        self,
        *,
        max_messages_before_end: int | None = None,
    ) -> None:
        self.max_messages_before_end = max_messages_before_end or int(
            os.getenv(ENV_REFLECTION_MAX_MESSAGES, str(DEFAULT_REFLECTION_MAX_MESSAGES))
        )



def get_model_provider() -> Provider:
    model_provider = os.getenv(ENV_MODEL_PROVIDER, DEFAULT_MODEL_PROVIDER).lower()
    try:
        return Provider(model_provider)
    except ValueError:
        raise ValueError(f"Unknown model provider: {model_provider}")
