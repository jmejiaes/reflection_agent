"""
Configuración cargada desde variables de entorno.
Facilita cambiar modelo, temperatura y API keys sin tocar código (LLMOps).
"""

import os
from functools import lru_cache
from enum import Enum
from dotenv import load_dotenv

load_dotenv()

# Variables de entorno globales, las de proveedor viven en cada estrategia
ENV_MODEL_PROVIDER = "MODEL_PROVIDER"
ENV_REFLECTION_MAX_MESSAGES = "REFLECTION_MAX_MESSAGES"

DEFAULT_MODEL_PROVIDER = "openai"
DEFAULT_REFLECTION_MAX_MESSAGES = 6

class Provider(str, Enum):
    openai = "openai"
    anthropic = "anthropic"


# El decorador @lru_cache(maxsize=1) guarda en memoria el resultado de la función decorada
# la primera vez que se llama, y devuelve ese mismo resultado en futuras llamadas.
# Así, get_settings() solo creará una instancia de Settings una vez (singleton sencillo).
@lru_cache(maxsize=1)
def get_settings() -> "Settings":
    return Settings()


class Settings:
    """Configuración del agente (la aplicación).

    Lo respectivo al LLM (modelo, API key, ...) lo resuelve la estrategia por proveedor.
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
        raise ValueError(f"Proveedor de modelo desconocido: {model_provider}")
