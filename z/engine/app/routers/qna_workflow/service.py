"""
QnA Workflow Service - Chain-based orchestration for question answering.

This service implements a simple chain-based approach where:
1. Input validation
2. LLM processing
3. Response formatting
"""

from loguru import logger

from app.schemas.common import TrackingMetadata
from app.services.llm_service import get_llm_service
from app.utilities.message_trimmer import get_trimming_stats, trim_messages


class WorkflowService:
    """
    Chain-based workflow service for QnA processing.

    This implements a simple sequential chain:
    - Validate input
    - Process with LLM
    - Format response
    """

    def __init__(self):
        """Initialize workflow service."""
        self.llm_service = get_llm_service()
        logger.info("WorkflowService initialized | Mode: Chain-based")

    async def process_question(
        self,
        message: str,
        context: dict | None = None,
        tracking: TrackingMetadata | None = None,
        conversation_history: list[dict[str, str]] | None = None,
    ) -> tuple[str, dict]:
        """
        Process a question using chain-based workflow.

        Chain steps:
        1. Validate input
        2. Trim conversation history to manage context window
        3. Call LLM service with trimmed conversation history
        4. Format response

        Args:
            message: The question to process
            context: Optional context
            tracking: Tracking metadata
            conversation_history: Previous messages in OpenAI format [{"role": "user/assistant", "content": "..."}]

        Returns:
            Tuple of (response_text, metadata)
        """
        original_history_length = len(conversation_history) if conversation_history else 0

        logger.info(
            f"[WorkflowService] Processing started | "
            f"Message length: {len(message)} | "
            f"conversation_history_length={original_history_length} | "
            f"Chat ID: {tracking.chat_id if tracking else 'none'}"
        )

        # Step 1: Validate input (simple validation for now)
        if not message or len(message.strip()) == 0:
            raise ValueError("Message cannot be empty")

        # Step 2: Trim conversation history if enabled
        trimmed_history = None
        if conversation_history:
            trimmed_history = trim_messages(conversation_history)

            # Log trimming stats
            trimming_stats = get_trimming_stats(
                original_count=original_history_length, trimmed_count=len(trimmed_history)
            )

            logger.info(
                f"[WorkflowService] Conversation history trimmed | "
                f"Original: {trimming_stats['original_count']} | "
                f"Trimmed: {trimming_stats['trimmed_count']} | "
                f"Removed: {trimming_stats['messages_removed']} | "
                f"Enabled: {trimming_stats['trimming_enabled']} | "
                f"Keep last: {trimming_stats['keep_last']}"
            )
        else:
            logger.debug("[WorkflowService] No conversation history provided")

        # Step 3: Process with LLM (including trimmed conversation history)
        response_text, metadata = await self.llm_service.process(
            message=message,
            context=context,
            tracking=tracking,
            conversation_history=trimmed_history,
        )

        # Step 4: Add workflow metadata
        metadata["orchestration"] = {
            "mode": "workflow",
            "type": "chain-based",
            "steps": ["validation", "message_trimming", "llm_processing", "formatting"],
        }

        # Add trimming stats to metadata if conversation history was provided
        if conversation_history:
            trimming_stats = get_trimming_stats(
                original_count=original_history_length, trimmed_count=len(trimmed_history) if trimmed_history else 0
            )
            metadata["message_trimming"] = trimming_stats

        logger.info(f"[WorkflowService] Processing complete | " f"Chat ID: {tracking.chat_id if tracking else 'none'}")

        return response_text, metadata


# Singleton instance
_workflow_service: WorkflowService | None = None


def get_workflow_service() -> WorkflowService:
    """
    Get singleton workflow service instance.

    Returns:
        WorkflowService instance
    """
    global _workflow_service
    if _workflow_service is None:
        _workflow_service = WorkflowService()
    return _workflow_service
