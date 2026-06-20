"""
Engine Configuration Module

This module imports settings from the centralized configs/settings.py
and exposes them with a clean interface for the engine service.
"""

import sys
from pathlib import Path


# Add project root to path to import configs
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from configs.settings import get_engine_settings


# Get settings instance
_settings = get_engine_settings()


class Settings:
    """
    Engine settings wrapper that exposes centralized settings
    for the engine service.
    """

    @property
    def host(self) -> str:
        return _settings.engine_host

    @property
    def port(self) -> int:
        return _settings.engine_port

    @property
    def log_level(self) -> str:
        return _settings.constants.get("logging", {}).get("level", "INFO")

    @property
    def cors_origins(self) -> list[str]:
        """CORS origins - restricted to backend only"""
        return _settings.cors_origins_list

    @property
    def mode(self) -> str:
        """Get current environment mode (local/dev)"""
        return _settings.mode

    @property
    def reload(self) -> bool:
        """Get reload setting based on mode"""
        return _settings.engine_reload

    @property
    def constants(self):
        """Access YAML constants directly"""
        return _settings.constants

    @property
    def processor_type(self) -> str:
        """Get processor type from constants"""
        return _settings.constants.get("processor", {}).get("type", "echo")

    @property
    def max_message_length(self) -> int:
        """Get max message length from constants"""
        return _settings.constants.get("processor", {}).get("max_message_length", 10000)

    @property
    def response_prefix(self) -> str:
        """Get response prefix from constants"""
        return _settings.constants.get("processor", {}).get("response_prefix", "Echo: ")

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

    @property
    def memory(self):
        """Access Memory settings"""
        return _settings.memory

    # LLM Configuration
    @property
    def engine_llm_temperature(self) -> float:
        """Get LLM temperature setting"""
        return _settings.engine_llm_temperature

    @property
    def engine_llm_timeout(self) -> int:
        """Get LLM request timeout in seconds"""
        return _settings.engine_llm_timeout

    @property
    def engine_llm_streaming(self) -> bool:
        """Get LLM streaming mode setting"""
        return _settings.engine_llm_streaming

    @property
    def engine_http_ssl_verify(self) -> bool:
        """Get HTTP SSL verification setting"""
        return _settings.engine_http_ssl_verify

    # Agent Configuration
    @property
    def agent_max_messages_before_summary(self) -> int:
        """Get max messages before summarization"""
        return _settings.agent_max_messages_before_summary

    @property
    def agent_messages_to_keep_after_summary(self) -> int:
        """Get messages to keep after summarization"""
        return _settings.agent_messages_to_keep_after_summary

    @property
    def agent_summary_message_count(self) -> int:
        """Get number of messages to include in summary"""
        return _settings.agent_summary_message_count

    @property
    def agent_summary_max_length(self) -> int:
        """Get maximum character length for summary"""
        return _settings.agent_summary_max_length


# Singleton instance
settings = Settings()
