"""
Message Trimmer Utility

This module provides utilities for trimming conversation history to manage
context window size. It supports OpenAI message format and uses the same
configuration as LangGraph memory management.

Configuration:
- LANGGRAPH_MESSAGE_TRIM_ENABLED: Enable/disable message trimming
- LANGGRAPH_MESSAGE_TRIM_KEEP_LAST: Number of recent messages to keep
"""

from loguru import logger

from app.config import settings


def trim_messages(
    messages: list[dict[str, str]], keep_last: int | None = None, trim_enabled: bool | None = None
) -> list[dict[str, str]]:
    """
    Trim conversation history to manage context window size.

    This function implements the same trimming strategy as LangGraph memory manager:
    - Keep all system messages (role="system")
    - Keep last N user/assistant messages

    Args:
        messages: List of messages in OpenAI format [{"role": "user/assistant/system", "content": "..."}]
        keep_last: Number of recent messages to keep (overrides config if provided)
        trim_enabled: Enable/disable trimming (overrides config if provided)

    Returns:
        Trimmed list of messages in OpenAI format
    """
    # Use config values if not explicitly provided
    if trim_enabled is None:
        trim_enabled = settings.postgres.langgraph_message_trim_enabled

    if keep_last is None:
        keep_last = settings.postgres.langgraph_message_trim_keep_last

    # If trimming is disabled, return original messages
    if not trim_enabled:
        logger.debug("[MessageTrimmer] Trimming disabled in configuration")
        return messages

    # If no trimming needed (messages count <= keep_last), return original
    if len(messages) <= keep_last:
        logger.debug(f"[MessageTrimmer] No trimming needed | " f"Messages: {len(messages)} | Keep last: {keep_last}")
        return messages

    original_count = len(messages)

    try:
        # Separate system messages from user/assistant messages
        system_messages = [msg for msg in messages if msg.get("role") == "system"]
        non_system_messages = [msg for msg in messages if msg.get("role") != "system"]

        # Keep last N non-system messages
        if keep_last > 0 and len(non_system_messages) > keep_last:
            recent_messages = non_system_messages[-keep_last:]

            # Combine system messages with recent messages
            trimmed = system_messages + recent_messages

            logger.info(
                f"[MessageTrimmer] Messages trimmed | "
                f"Original: {original_count} | "
                f"Kept: {len(trimmed)} | "
                f"System: {len(system_messages)} | "
                f"Recent: {len(recent_messages)} | "
                f"Strategy: keep_last_{keep_last}"
            )

            return trimmed

        # No trimming needed
        return messages

    except Exception as e:
        logger.warning(f"[MessageTrimmer] Trimming failed | Error: {e!s}")
        return messages  # Return original on error


def trim_openai_messages(
    conversation_history: list[dict[str, str]],
    current_message: str,
    keep_last: int | None = None,
    trim_enabled: bool | None = None,
) -> list[dict[str, str]]:
    """
    Trim conversation history and prepare it for LLM call.

    This is a convenience function that:
    1. Adds the current message to the conversation history
    2. Trims the combined messages
    3. Returns the trimmed conversation history (without current message)

    The current message is excluded from the trimmed output because it will be
    added separately in the LLM service along with the system prompt.

    Args:
        conversation_history: Previous messages in OpenAI format
        current_message: Current user message to add
        keep_last: Number of recent messages to keep (overrides config)
        trim_enabled: Enable/disable trimming (overrides config)

    Returns:
        Trimmed conversation history (excluding current message)
    """
    # Use config values if not explicitly provided
    if keep_last is None:
        keep_last = settings.postgres.langgraph_message_trim_keep_last

    # Create combined message list
    all_messages = (conversation_history or []) + [{"role": "user", "content": current_message}]

    # Trim all messages
    trimmed_all = trim_messages(all_messages, keep_last=keep_last, trim_enabled=trim_enabled)

    # Remove the current message (last message) and return
    # The current message will be added back in LLMService
    if trimmed_all and trimmed_all[-1].get("content") == current_message:
        return trimmed_all[:-1]

    # Fallback: return trimmed history without current message
    return trimmed_all


def get_trimming_stats(original_count: int, trimmed_count: int, keep_last: int | None = None) -> dict[str, any]:
    """
    Get statistics about message trimming.

    Args:
        original_count: Original message count
        trimmed_count: Trimmed message count
        keep_last: Configured keep_last value

    Returns:
        Dictionary with trimming statistics
    """
    if keep_last is None:
        keep_last = settings.postgres.langgraph_message_trim_keep_last

    return {
        "trimming_enabled": settings.postgres.langgraph_message_trim_enabled,
        "keep_last": keep_last,
        "original_count": original_count,
        "trimmed_count": trimmed_count,
        "messages_removed": max(0, original_count - trimmed_count),
        "trim_applied": original_count > trimmed_count,
    }
