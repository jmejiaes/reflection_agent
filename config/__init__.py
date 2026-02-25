"""Centralized configuration for LLMOps (model, env, parameters)."""

from config.settings import get_settings

# This ensures 'from config import *' only exposes get_settings,
# and makes the package's public API explicit
__all__ = ["get_settings"]
