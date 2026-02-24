"""Configuración centralizada para LLMOps (modelo, env, parámetros)."""

from config.settings import get_settings

# Esto hace que cuando alguien haga 'from config import *' solo tendrá get_settings,
# y esto además deja claro qué es lo "oficial" del paquete
__all__ = ["get_settings"]
