"""
Backend Configuration Module

This module imports settings from the centralized configs/settings.py
and exposes them with a backward-compatible interface.
"""

import sys
from pathlib import Path


# Add project root to path to import configs
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from configs.settings import get_backend_settings


# Get settings instance
_settings = get_backend_settings()


class Settings:
    """
    Backward-compatible settings wrapper that exposes centralized settings
    with the same interface as the old config.
    """

    @property
    def host(self) -> str:
        return _settings.backend_host

    @property
    def port(self) -> int:
        return _settings.backend_port

    @property
    def log_level(self) -> str:
        return _settings.constants.get("logging", {}).get("level", "INFO")

    @property
    def engine_url(self) -> str:
        return _settings.backend_engine_url

    @property
    def engine_timeout(self) -> int:
        timeout = _settings.constants.get("timeouts", {}).get("engine_request_seconds", 30)
        return timeout

    @property
    def cors_origins(self) -> list[str]:
        return _settings.cors_origins_list

    @property
    def mode(self) -> str:
        """Get current environment mode (local/dev)"""
        return _settings.mode

    @property
    def reload(self) -> bool:
        """Get reload setting based on mode"""
        return _settings.backend_reload

    @property
    def constants(self):
        """Access YAML constants directly"""
        return _settings.constants

    # Infrastructure settings
    @property
    def postgres(self):
        """Access PostgreSQL settings"""
        return _settings.postgres

    @property
    def redis(self):
        """Access Redis settings"""
        return _settings.redis

    @property
    def langfuse(self):
        """Access Langfuse settings"""
        return _settings.langfuse

    @property
    def litellm(self):
        """Access LiteLLM settings"""
        return _settings.litellm

    @property
    def azure_openai(self):
        """Access Azure OpenAI settings"""
        return _settings.azure_openai

    @property
    def azure_ai(self):
        """Access Azure AI settings"""
        return _settings.azure_ai


# Singleton instance
settings = Settings()
