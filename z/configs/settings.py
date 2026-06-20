"""
Centralized Configuration Management

This module provides a centralized configuration system that:
1. Loads environment variables from .env file
2. Loads constants from YAML files (frontend.yaml, backend.yaml, engine.yaml)
3. Provides typed settings objects for each service
4. Supports hot reload in local mode
5. Manages MODE-based configuration (local/dev)
"""

from pathlib import Path
from typing import Any, Literal, Optional

import yaml
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


# Base paths
PROJECT_ROOT = Path(__file__).parent.parent
CONFIGS_DIR = Path(__file__).parent


class BaseAppSettings(BaseSettings):
    """Base settings class with common configuration"""

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow",
    )

    # Environment Mode
    mode: Literal["local", "dev"] = Field(default="local", description="Environment mode: local or dev")


# ============================================================================
# Infrastructure Settings Classes
# ============================================================================


class PostgreSQLSettings(BaseSettings):
    """PostgreSQL database configuration"""

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow",
    )

    postgres_user: str = Field(default="postgres")
    postgres_password: str = Field(default="postgres")
    postgres_db: str = Field(default="postgres")

    # Main database
    main_db_name: str = Field(default="main_db")
    main_db_user: str = Field(default="main_user")
    main_db_password: str = Field(default="main_password")

    # Langfuse database
    langfuse_db_name: str = Field(default="langfuse")
    langfuse_db_user: str = Field(default="langfuse")
    langfuse_db_password: str = Field(default="langfuse_password")

    # LiteLLM database
    litellm_db_name: str = Field(default="litellm")
    litellm_db_user: str = Field(default="litellm")
    litellm_db_password: str = Field(default="litellm_password")

    # LangGraph database (Agent Memory & Checkpointing)
    langgraph_db_name: str = Field(default="langgraph")
    langgraph_db_user: str = Field(default="langgraph")
    langgraph_db_password: str = Field(default="langgraph_password")

    # LangGraph Memory Configuration
    langgraph_memory_enabled: bool = Field(default=True)
    langgraph_message_trim_enabled: bool = Field(default=True)
    langgraph_message_trim_keep_last: int = Field(default=5)
    langgraph_message_trim_max_tokens: int = Field(default=4000)

    @property
    def main_database_url(self) -> str:
        """Get main database connection URL"""
        return f"postgresql://{self.main_db_user}:{self.main_db_password}@postgres:5432/{self.main_db_name}"

    @property
    def langfuse_database_url(self) -> str:
        """Get Langfuse database connection URL"""
        return f"postgresql://{self.langfuse_db_user}:{self.langfuse_db_password}@postgres:5432/{self.langfuse_db_name}"

    @property
    def litellm_database_url(self) -> str:
        """Get LiteLLM database connection URL"""
        return f"postgresql://{self.litellm_db_user}:{self.litellm_db_password}@postgres:5432/{self.litellm_db_name}"

    @property
    def langgraph_database_url(self) -> str:
        """Get LangGraph database connection URL"""
        return (
            f"postgresql://{self.langgraph_db_user}:{self.langgraph_db_password}@postgres:5432/{self.langgraph_db_name}"
        )

    @property
    def langgraph_async_database_url(self) -> str:
        """Get LangGraph async database connection URL for asyncpg"""
        return f"postgresql+asyncpg://{self.langgraph_db_user}:{self.langgraph_db_password}@postgres:5432/{self.langgraph_db_name}"


class RedisSettings(BaseSettings):
    """Redis configuration"""

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow",
    )

    redis_host: str = Field(default="redis-stack")
    redis_port: int = Field(default=6379)
    redis_password: str = Field(default="")
    redis_max_memory: str = Field(default="1024mb")

    @property
    def main_redis_url(self) -> str:
        """Main Redis URL (DB 0)"""
        auth = f":{self.redis_password}@" if self.redis_password else ""
        return f"redis://{auth}{self.redis_host}:{self.redis_port}/0"

    @property
    def langfuse_redis_url(self) -> str:
        """Langfuse Redis URL (DB 1)"""
        auth = f":{self.redis_password}@" if self.redis_password else ""
        return f"redis://{auth}{self.redis_host}:{self.redis_port}/1"

    @property
    def litellm_redis_url(self) -> str:
        """LiteLLM Redis URL (DB 2)"""
        auth = f":{self.redis_password}@" if self.redis_password else ""
        return f"redis://{auth}{self.redis_host}:{self.redis_port}/2"


class LangfuseSettings(BaseSettings):
    """Langfuse observability platform configuration"""

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow",
    )

    # Explicit enable/disable flag
    langfuse_enabled: bool = Field(default=True, description="Enable/disable Langfuse tracing")

    langfuse_public_key: str = Field(default="")
    langfuse_secret_key: str = Field(default="")
    langfuse_host: str = Field(default="http://langfuse-web:3000")

    langfuse_nextauth_secret: str = Field(default="")
    langfuse_encryption_key: str = Field(default="")
    langfuse_salt: str = Field(default="")

    langfuse_init_org_id: str = Field(default="zuna-org")
    langfuse_init_org_name: str = Field(default="Zuna Organization")

    langfuse_init_project_id: str = Field(default="zuna-project")
    langfuse_init_project_name: str = Field(default="Zuna Project")
    langfuse_init_project_public_key: str = Field(default="")
    langfuse_init_project_secret_key: str = Field(default="")

    langfuse_init_user_email: str = Field(default="admin@example.com")
    langfuse_init_user_name: str = Field(default="Admin")
    langfuse_init_user_password: str = Field(default="admin123")

    @property
    def is_enabled(self) -> bool:
        """
        Check if Langfuse is enabled and properly configured.

        Langfuse is enabled if:
        1. LANGFUSE_ENABLED is true (explicit flag)
        2. AND both public_key and secret_key are configured
        """
        return self.langfuse_enabled and bool(self.langfuse_public_key) and bool(self.langfuse_secret_key)


class LiteLLMSettings(BaseSettings):
    """LiteLLM proxy configuration"""

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow",
    )

    # Explicit enable/disable flag
    litellm_enabled: bool = Field(default=True, description="Enable/disable LiteLLM proxy")

    # Proxy configuration
    litellm_master_key: str = Field(default="sk-1234")
    litellm_salt_key: str = Field(default="sk-salt-1234")
    litellm_base_url: str = Field(default="http://litellm:4000")
    litellm_ui_username: str = Field(default="admin")
    litellm_ui_password: str = Field(default="admin123")

    # Model names (when LiteLLM enabled)
    litellm_chat_model: str = Field(default="gpt-4.1")
    litellm_embedding_model: str = Field(default="text-embedding-3-small")
    litellm_rerank_model: str = Field(default="cohere-rerank-v3.5")

    @property
    def is_enabled(self) -> bool:
        """
        Check if LiteLLM is enabled and properly configured.

        LiteLLM is enabled if:
        1. LITELLM_ENABLED is true (explicit flag)
        2. AND master_key and base_url are configured
        """
        return self.litellm_enabled and bool(self.litellm_master_key) and bool(self.litellm_base_url)


class AzureOpenAISettings(BaseSettings):
    """Azure OpenAI configuration (fallback when LiteLLM disabled)"""

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow",
    )

    azure_openai_endpoint: str = Field(default="")
    azure_openai_api_key: str = Field(default="")
    azure_openai_api_version: str = Field(default="2024-08-01-preview")

    # Azure OpenAI deployment names (when LiteLLM disabled)
    azure_openai_chat_deployment: str = Field(default="gpt-4")
    azure_openai_embedding_deployment: str = Field(default="text-embedding-3-small")

    @property
    def is_enabled(self) -> bool:
        """Check if Azure OpenAI is properly configured"""
        return bool(self.azure_openai_endpoint and self.azure_openai_api_key)


class AzureAISettings(BaseSettings):
    """Azure AI (Cohere Rerank) configuration"""

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow",
    )

    azure_ai_api_base: str = Field(default="")
    azure_ai_api_key: str = Field(default="")

    @property
    def is_enabled(self) -> bool:
        """Check if Azure AI is properly configured"""
        return bool(self.azure_ai_api_base and self.azure_ai_api_key)


class MemorySettings(BaseSettings):
    """Memory system (Mem0) configuration"""

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow",
    )

    # Explicit enable/disable flag
    memory_enabled: bool = Field(default=False, description="Enable/disable memory system (Mem0)")

    @property
    def is_enabled(self) -> bool:
        """
        Check if memory system is enabled.

        Currently just checks the flag.
        Future: Will also check for Mem0 API keys and configuration.
        """
        return self.memory_enabled


class FrontendSettings(BaseAppSettings):
    """Frontend-specific settings combining env vars and YAML constants"""

    # Environment variables
    vite_backend_url: str = Field(default="http://localhost:8000", description="Backend API URL for frontend")

    # YAML constants (loaded separately)
    constants: dict[str, Any] = Field(default_factory=dict)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Load YAML constants
        yaml_path = CONFIGS_DIR / "frontend.yaml"
        if yaml_path.exists():
            with open(yaml_path) as f:
                self.constants = yaml.safe_load(f) or {}


class BackendSettings(BaseAppSettings):
    """Backend-specific settings combining env vars and YAML constants"""

    # Environment variables
    backend_engine_url: str = Field(default="http://localhost:8001", description="Engine service URL")

    backend_cors_origins: str = Field(
        default='["http://localhost:5173"]',
        description="CORS origins for backend (JSON array string)",
    )

    # Server configuration (overridden by MODE)
    backend_host: str = Field(default="0.0.0.0", description="Backend server host")
    backend_port: int = Field(default=8000, description="Backend server port")
    backend_reload: bool = Field(default=True, description="Enable auto-reload (local mode only)")

    # YAML constants (loaded separately)
    constants: dict[str, Any] = Field(default_factory=dict)

    # Infrastructure settings (lazy loaded)
    _postgres: PostgreSQLSettings | None = None
    _redis: RedisSettings | None = None
    _langfuse: LangfuseSettings | None = None
    _litellm: LiteLLMSettings | None = None
    _azure_openai: AzureOpenAISettings | None = None
    _azure_ai: AzureAISettings | None = None
    _memory: Optional["MemorySettings"] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Load YAML constants
        yaml_path = CONFIGS_DIR / "backend.yaml"
        if yaml_path.exists():
            with open(yaml_path) as f:
                self.constants = yaml.safe_load(f) or {}

        # Override reload based on MODE
        if self.mode == "dev":
            self.backend_reload = False

    @property
    def cors_origins_list(self) -> list[str]:
        """Parse CORS origins from JSON string to list"""
        import json

        try:
            return json.loads(self.backend_cors_origins)
        except json.JSONDecodeError:
            return ["http://localhost:5173"]

    @property
    def postgres(self) -> PostgreSQLSettings:
        """Get PostgreSQL settings"""
        if self._postgres is None:
            self._postgres = PostgreSQLSettings()
        return self._postgres

    @property
    def redis(self) -> RedisSettings:
        """Get Redis settings"""
        if self._redis is None:
            self._redis = RedisSettings()
        return self._redis

    @property
    def langfuse(self) -> LangfuseSettings:
        """Get Langfuse settings"""
        if self._langfuse is None:
            self._langfuse = LangfuseSettings()
        return self._langfuse

    @property
    def litellm(self) -> LiteLLMSettings:
        """Get LiteLLM settings"""
        if self._litellm is None:
            self._litellm = LiteLLMSettings()
        return self._litellm

    @property
    def azure_openai(self) -> AzureOpenAISettings:
        """Get Azure OpenAI settings"""
        if self._azure_openai is None:
            self._azure_openai = AzureOpenAISettings()
        return self._azure_openai

    @property
    def azure_ai(self) -> AzureAISettings:
        """Get Azure AI settings"""
        if self._azure_ai is None:
            self._azure_ai = AzureAISettings()
        return self._azure_ai

    @property
    def memory(self) -> "MemorySettings":
        """Get Memory settings"""
        if self._memory is None:
            self._memory = MemorySettings()
        return self._memory


class EngineSettings(BaseAppSettings):
    """Engine-specific settings combining env vars and YAML constants"""

    # Environment variables
    engine_cors_origins: str = Field(
        default='["http://localhost:8000"]',
        description="CORS origins for engine (JSON array string) - only backend",
    )

    # Server configuration (overridden by MODE)
    engine_host: str = Field(default="0.0.0.0", description="Engine server host")
    engine_port: int = Field(default=8001, description="Engine server port")
    engine_reload: bool = Field(default=True, description="Enable auto-reload (local mode only)")

    # LLM Configuration
    engine_llm_temperature: float = Field(
        default=0.7, description="LLM temperature (0.0 = deterministic, 2.0 = very creative)"
    )
    engine_llm_timeout: int = Field(default=60, description="LLM request timeout in seconds")
    engine_llm_streaming: bool = Field(default=False, description="Enable/disable streaming mode")
    engine_http_ssl_verify: bool = Field(default=False, description="Enable/disable SSL verification for HTTP clients")

    # Agent Configuration
    agent_max_messages_before_summary: int = Field(
        default=10, description="Maximum messages before triggering conversation summarization"
    )
    agent_messages_to_keep_after_summary: int = Field(
        default=2, description="Number of messages to keep after summarization"
    )
    agent_summary_message_count: int = Field(default=5, description="Number of recent messages to include in summary")
    agent_summary_max_length: int = Field(default=200, description="Maximum character length for summary content")

    # YAML constants (loaded separately)
    constants: dict[str, Any] = Field(default_factory=dict)

    # Infrastructure settings (lazy loaded)
    _postgres: PostgreSQLSettings | None = None
    _redis: RedisSettings | None = None
    _langfuse: LangfuseSettings | None = None
    _litellm: LiteLLMSettings | None = None
    _azure_openai: AzureOpenAISettings | None = None
    _azure_ai: AzureAISettings | None = None
    _memory: Optional["MemorySettings"] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Load YAML constants
        yaml_path = CONFIGS_DIR / "engine.yaml"
        if yaml_path.exists():
            with open(yaml_path) as f:
                self.constants = yaml.safe_load(f) or {}

        # Override reload based on MODE
        if self.mode == "dev":
            self.engine_reload = False

    @property
    def cors_origins_list(self) -> list[str]:
        """Parse CORS origins from JSON string to list"""
        import json

        try:
            return json.loads(self.engine_cors_origins)
        except json.JSONDecodeError:
            return ["http://localhost:8000"]

    @property
    def postgres(self) -> PostgreSQLSettings:
        """Get PostgreSQL settings"""
        if self._postgres is None:
            self._postgres = PostgreSQLSettings()
        return self._postgres

    @property
    def redis(self) -> RedisSettings:
        """Get Redis settings"""
        if self._redis is None:
            self._redis = RedisSettings()
        return self._redis

    @property
    def langfuse(self) -> LangfuseSettings:
        """Get Langfuse settings"""
        if self._langfuse is None:
            self._langfuse = LangfuseSettings()
        return self._langfuse

    @property
    def litellm(self) -> LiteLLMSettings:
        """Get LiteLLM settings"""
        if self._litellm is None:
            self._litellm = LiteLLMSettings()
        return self._litellm

    @property
    def azure_openai(self) -> AzureOpenAISettings:
        """Get Azure OpenAI settings"""
        if self._azure_openai is None:
            self._azure_openai = AzureOpenAISettings()
        return self._azure_openai

    @property
    def azure_ai(self) -> AzureAISettings:
        """Get Azure AI settings"""
        if self._azure_ai is None:
            self._azure_ai = AzureAISettings()
        return self._azure_ai

    @property
    def memory(self) -> "MemorySettings":
        """Get Memory settings"""
        if self._memory is None:
            self._memory = MemorySettings()
        return self._memory


# Singleton instances
_frontend_settings: FrontendSettings | None = None
_backend_settings: BackendSettings | None = None
_engine_settings: EngineSettings | None = None


def get_frontend_settings() -> FrontendSettings:
    """Get or create frontend settings singleton"""
    global _frontend_settings
    if _frontend_settings is None:
        _frontend_settings = FrontendSettings()
    return _frontend_settings


def get_backend_settings() -> BackendSettings:
    """Get or create backend settings singleton"""
    global _backend_settings
    if _backend_settings is None:
        _backend_settings = BackendSettings()
    return _backend_settings


def get_engine_settings() -> EngineSettings:
    """Get or create engine settings singleton"""
    global _engine_settings
    if _engine_settings is None:
        _engine_settings = EngineSettings()
    return _engine_settings


def reload_settings():
    """Reload all settings (useful for hot reload in local mode)"""
    global _frontend_settings, _backend_settings, _engine_settings
    _frontend_settings = None
    _backend_settings = None
    _engine_settings = None


# Convenience exports
frontend_settings = get_frontend_settings()
backend_settings = get_backend_settings()
engine_settings = get_engine_settings()


if __name__ == "__main__":
    """Test settings loading"""
    print("=== Frontend Settings ===")
    print(f"Mode: {frontend_settings.mode}")
    print(f"Backend URL: {frontend_settings.vite_backend_url}")
    print(f"Constants: {frontend_settings.constants.keys()}")

    print("\n=== Backend Settings ===")
    print(f"Mode: {backend_settings.mode}")
    print(f"Engine URL: {backend_settings.backend_engine_url}")
    print(f"CORS Origins: {backend_settings.cors_origins_list}")
    print(f"Reload: {backend_settings.backend_reload}")
    print(f"Constants: {backend_settings.constants.keys()}")

    print("\n=== Engine Settings ===")
    print(f"Mode: {engine_settings.mode}")
    print(f"CORS Origins: {engine_settings.cors_origins_list}")
    print(f"Reload: {engine_settings.engine_reload}")
    print(f"Constants: {engine_settings.constants.keys()}")
