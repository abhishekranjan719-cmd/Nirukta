"""
LLM Service - Core LLM integration and processing logic.

This service provides a unified interface for LLM operations with support for:
- Multiple LLM providers (LiteLLM proxy, Azure OpenAI direct)
- Observability via Langfuse
- Comprehensive tracking and metadata
"""

from datetime import datetime

from loguru import logger

from app.clients import get_azure_openai_client, get_langfuse_client, get_litellm_client
from app.config import settings
from app.schemas.common import TrackingMetadata
from app.utilities.prompt_loader import get_prompt_loader


class LLMService:
    """
    Core LLM service with provider abstraction and observability.

    Features:
    - Multi-provider support (LiteLLM proxy, Azure OpenAI)
    - Automatic provider selection based on configuration
    - Full Langfuse tracing for observability
    - Comprehensive metadata tracking
    - Error handling and fallbacks
    - Prompt management via PromptLoader
    """

    def __init__(self, system_prompt: str | None = None):
        """
        Initialize LLM service.

        Args:
            system_prompt: Optional system prompt. If None, loads formatter_prompt.md

        Chooses between:
        - LiteLLM proxy (if LITELLM_ENABLED=true)
        - Azure OpenAI direct (if LITELLM_ENABLED=false)
        """
        # Load system prompt
        if system_prompt is None:
            prompt_loader = get_prompt_loader()
            self.system_prompt = prompt_loader.load_formatter_prompt()
        else:
            self.system_prompt = system_prompt
            logger.info(f"Using provided system prompt | Length: {len(system_prompt)} chars")

        # Determine which client to use
        self.use_litellm = settings.litellm.is_enabled

        if self.use_litellm:
            # Use LiteLLM proxy
            self.llm_client = get_litellm_client()
            self.model = settings.litellm.litellm_chat_model
            self.client_type = "LiteLLM Proxy"
        else:
            # Use Azure OpenAI direct
            self.llm_client = get_azure_openai_client()
            self.model = settings.azure_openai.azure_openai_chat_deployment
            self.client_type = "Azure OpenAI Direct"

        self.langfuse_client = get_langfuse_client()
        self.temperature = settings.engine_llm_temperature

        logger.info(
            f"LLMService initialized | "
            f"Client: {self.client_type} | "
            f"Model: {self.model} | "
            f"Temperature: {self.temperature} | "
            f"Langfuse enabled: {self.langfuse_client.enabled}"
        )

    async def process(
        self,
        message: str,
        context: dict | None = None,
        tracking: TrackingMetadata | None = None,
        conversation_history: list[dict[str, str]] | None = None,
    ) -> tuple[str, dict]:
        """
        Process a message using LLM and return response with metadata.

        Flow:
        1. Prepare messages for LLM with conversation history
        2. Call LLM client (LiteLLM proxy OR Azure OpenAI direct)
        3. Log LLM generation to Langfuse (if enabled)
        4. Return response with comprehensive metadata

        Args:
            message: The input message to process
            context: Optional context for processing
            tracking: Tracking metadata for observability
            conversation_history: Previous messages in OpenAI format [{"role": "user/assistant", "content": "..."}]

        Returns:
            Tuple of (response_text, metadata_dict)
        """
        start_time = datetime.now()

        try:
            # Prepare messages for LLM with formatter prompt
            # TODO: Consume system prompt from Langfuse prompt management when configured
            #       instead of loading from local file. This will enable:
            #       - Centralized prompt versioning and management
            #       - A/B testing of different prompt variations
            #       - Dynamic prompt updates without redeployment
            messages = [
                {
                    "role": "system",
                    "content": self.system_prompt,
                },
            ]

            # Add conversation history if provided
            if conversation_history:
                messages.extend(conversation_history)

            # Add current user message
            messages.append({"role": "user", "content": message})

            # Call LLM (proxy or direct)
            logger.info(
                f"Calling {self.client_type} | "
                f"Model: {self.model} | "
                f"Chat ID: {tracking.chat_id if tracking else 'none'}"
            )

            llm_response = await self.llm_client.chat_completion(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
            )

            # Extract response
            response_text = llm_response["choices"][0]["message"]["content"]
            usage = llm_response.get("usage", {})

            # Calculate processing time
            end_time = datetime.now()
            processing_time = (end_time - start_time).total_seconds()

            # Log to Langfuse if tracking provided
            if tracking and self.langfuse_client.enabled:
                self.langfuse_client.log_llm_call(
                    tracking=tracking,
                    model=self.model,
                    input_messages=messages,
                    output_message=response_text,
                    usage=usage,
                    temperature=self.temperature,
                    processing_time=processing_time,
                )

            # Build metadata
            metadata = {
                "processed_at": end_time.isoformat(),
                "processing_time_seconds": processing_time,
                "processing_type": "llm",
                "model": self.model,
                "temperature": self.temperature,
                "original_message_length": len(message),
                "response_length": len(response_text),
                "tokens": {
                    "prompt": usage.get("prompt_tokens", 0),
                    "completion": usage.get("completion_tokens", 0),
                    "total": usage.get("total_tokens", 0),
                },
            }

            # Add tracking IDs to metadata if provided
            if tracking:
                metadata["tracking"] = {
                    "user_id": tracking.user_id,
                    "chat_id": tracking.chat_id,
                    "conversation_id": tracking.conversation_id,
                    "usecase_id": tracking.usecase_id,
                }

            logger.info(
                f"LLM processing complete | "
                f"Chat ID: {tracking.chat_id if tracking else 'none'} | "
                f"Time: {processing_time:.2f}s | "
                f"Tokens: {usage.get('total_tokens', 0)}"
            )

            return response_text, metadata

        except Exception as e:
            logger.error(
                f"LLM processing failed | " f"Chat ID: {tracking.chat_id if tracking else 'none'} | " f"Error: {e!s}"
            )

            # Fallback to echo response
            response = f"[LLM Error] I apologize, but I encountered an error processing your request. Original message: {message}"

            metadata = {
                "processed_at": datetime.now().isoformat(),
                "processing_type": "error_fallback",
                "error": str(e),
                "original_message_length": len(message),
            }

            if tracking:
                metadata["tracking"] = {
                    "user_id": tracking.user_id,
                    "chat_id": tracking.chat_id,
                    "conversation_id": tracking.conversation_id,
                    "usecase_id": tracking.usecase_id,
                }

            return response, metadata


# Singleton instance
_llm_service: LLMService | None = None


def get_llm_service(system_prompt: str | None = None) -> LLMService:
    """
    Get singleton LLM service instance.

    Args:
        system_prompt: Optional system prompt (only used on first initialization)

    Returns:
        LLMService instance
    """
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService(system_prompt=system_prompt)
    return _llm_service
