"""
Langfuse Client

This module provides Langfuse v3 SDK integration for LLM observability.
External API client for tracing and monitoring LLM calls.
"""

from langfuse import Langfuse
from loguru import logger

from app.config import settings
from app.schemas.common import TrackingMetadata


class LangfuseClient:
    """
    Langfuse v3 client for LLM observability.

    Features:
    - Manual trace/generation tracking
    - Comprehensive metadata tracking with all IDs and aliases
    - LLM request/response tracking
    - Token usage tracking
    - Cost tracking
    """

    def __init__(self):
        """Initialize Langfuse client with configuration from settings."""
        self.enabled = settings.langfuse.is_enabled

        if not self.enabled:
            logger.warning("Langfuse is not enabled | Set LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY")
            self.client = None
            return

        try:
            self.client = Langfuse(
                public_key=settings.langfuse.langfuse_public_key,
                secret_key=settings.langfuse.langfuse_secret_key,
                host=settings.langfuse.langfuse_host,
            )
            logger.info(f"Langfuse client initialized | Host: {settings.langfuse.langfuse_host}")
        except Exception as e:
            logger.error(f"Failed to initialize Langfuse client | Error: {e!s}")
            self.enabled = False
            self.client = None

    def log_llm_call(
        self,
        tracking: TrackingMetadata,
        model: str,
        input_messages: list[dict[str, str]],
        output_message: str,
        usage: dict[str, int] | None = None,
        temperature: float = 0.7,
        processing_time: float = 0.0,
    ) -> bool:
        """
        Log a complete LLM call to Langfuse with all tracking metadata.

        This is a simplified API that logs everything in one call.

        Args:
            tracking: TrackingMetadata with all IDs and aliases
            model: Model name (e.g., "gpt-4.1")
            input_messages: List of input messages
            output_message: Generated output message
            usage: Token usage dict with prompt_tokens, completion_tokens, total_tokens
            temperature: Model temperature parameter
            processing_time: Processing time in seconds

        Returns:
            True if successful, False otherwise
        """
        if not self.enabled or not self.client:
            return False

        try:
            # Build comprehensive metadata with all tracking IDs
            metadata = {
                # Primary IDs
                "user_id": tracking.user_id,
                "chat_id": tracking.chat_id,
                "conversation_id": tracking.conversation_id,
                "usecase_id": tracking.usecase_id,
                # chat_id aliases
                "request_id": tracking.request_id,
                "run_id": tracking.run_id,
                "correlation_id": tracking.correlation_id,
                "observation_id": tracking.observation_id,
                # conversation_id aliases
                "session_id": tracking.session_id,
                "thread_id": tracking.thread_id,
                # usecase_id aliases
                "app_id": tracking.app_id,
                "agent_id": tracking.agent_id,
                # user_id alias
                "user_email": tracking.user_email,
                # Additional metadata
                "model": model,
                "temperature": temperature,
                "processing_time_seconds": processing_time,
            }

            # Start a generation observation
            generation = self.client.start_generation(
                name="llm_generation",
                model=model,
                model_parameters={
                    "temperature": temperature,
                },
                input=input_messages,
                output=output_message,
                metadata=metadata,
                usage_details={
                    "input": usage.get("prompt_tokens", 0) if usage else 0,
                    "output": usage.get("completion_tokens", 0) if usage else 0,
                    "total": usage.get("total_tokens", 0) if usage else 0,
                }
                if usage
                else None,
            )

            # End the generation
            generation.end()

            logger.debug(
                f"Langfuse LLM call logged | "
                f"Trace ID: {tracking.chat_id} | "
                f"User: {tracking.user_id} | "
                f"Session: {tracking.conversation_id} | "
                f"Tokens: {usage.get('total_tokens', 0) if usage else 0}"
            )

            return True

        except Exception as e:
            logger.error(f"Failed to log Langfuse LLM call | Error: {e!s}")
            return False

    def flush(self):
        """
        Flush pending Langfuse events.

        Call this to ensure all events are sent before shutdown.
        """
        if not self.enabled or not self.client:
            return

        try:
            self.client.flush()
            logger.debug("Langfuse events flushed")
        except Exception as e:
            logger.error(f"Failed to flush Langfuse events | Error: {e!s}")


# Singleton instance
_langfuse_client: LangfuseClient | None = None


def get_langfuse_client() -> LangfuseClient:
    """
    Get or create singleton Langfuse client instance.

    Returns:
        LangfuseClient instance
    """
    global _langfuse_client
    if _langfuse_client is None:
        _langfuse_client = LangfuseClient()
    return _langfuse_client


# Backward compatibility alias
def get_langfuse_tracer() -> LangfuseClient:
    """Deprecated: Use get_langfuse_client() instead."""
    return get_langfuse_client()
