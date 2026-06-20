"""
LangGraph Memory Module - PostgreSQL Checkpointer and Store

This module implements production-ready memory management for LangGraph agents using:
1. AsyncPostgresSaver - For checkpointing (short-term conversation memory)
2. AsyncPostgresStore - For long-term memory storage
3. Message trimming - To manage context window size

Architecture:
- Multi-user, multi-conversation support
- Thread ID mapping to conversation_id
- Configurable message retention
- Async PostgreSQL for non-blocking operations

References:
- https://docs.langchain.com/oss/python/langgraph/add-memory
- https://pypi.org/project/langgraph-checkpoint-postgres/
"""

from contextlib import asynccontextmanager

from langchain_core.messages import BaseMessage
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langgraph.store.postgres.aio import AsyncPostgresStore
from loguru import logger

from app.config import settings


class LangGraphMemory:
    """
    Production-ready LangGraph memory manager with PostgreSQL backend.

    Features:
    - Async PostgreSQL checkpointer for conversation history
    - Async PostgreSQL store for long-term memory
    - Configurable message trimming
    - Multi-user, multi-conversation support
    - Thread ID alignment with application IDs
    """

    def __init__(self):
        """Initialize memory manager (lazy initialization pattern)."""
        self._checkpointer: AsyncPostgresSaver | None = None
        self._store: AsyncPostgresStore | None = None
        self._checkpointer_cm = None  # Context manager for cleanup
        self._store_cm = None  # Context manager for cleanup
        self._initialized = False

        logger.info(
            f"[LangGraphMemory] Initialized | "
            f"Memory enabled: {settings.postgres.langgraph_memory_enabled} | "
            f"Trim enabled: {settings.postgres.langgraph_message_trim_enabled} | "
            f"Keep last: {settings.postgres.langgraph_message_trim_keep_last}"
        )

    @property
    def is_enabled(self) -> bool:
        """Check if memory is enabled."""
        return settings.postgres.langgraph_memory_enabled

    async def initialize(self):
        """
        Initialize checkpointer and store with database connection.

        This should be called once during application startup.
        Creates required database tables if they don't exist.
        """
        if not self.is_enabled:
            logger.info("[LangGraphMemory] Memory disabled in configuration, skipping initialization")
            return

        if self._initialized:
            logger.debug("[LangGraphMemory] Already initialized")
            return

        try:
            # Get database connection string
            db_url = settings.postgres.langgraph_database_url

            logger.info(
                f"[LangGraphMemory] Initializing with PostgreSQL | Database: {settings.postgres.langgraph_db_name}"
            )

            # Initialize checkpointer (for conversation history)
            # from_conn_string returns async context manager, need to enter it first
            self._checkpointer_cm = AsyncPostgresSaver.from_conn_string(db_url)
            self._checkpointer = await self._checkpointer_cm.__aenter__()
            await self._checkpointer.setup()
            logger.info("[LangGraphMemory] Checkpointer initialized and schema created")

            # Initialize store (for long-term memory)
            self._store_cm = AsyncPostgresStore.from_conn_string(db_url)
            self._store = await self._store_cm.__aenter__()
            await self._store.setup()
            logger.info("[LangGraphMemory] Store initialized and schema created")

            self._initialized = True
            logger.info("[LangGraphMemory] Memory system ready for production use")

        except Exception as e:
            logger.error(f"[LangGraphMemory] Initialization failed | Error: {e!s}", exc_info=True)
            raise

    async def close(self):
        """Close database connections."""
        if self._checkpointer_cm and self._checkpointer:
            try:
                await self._checkpointer_cm.__aexit__(None, None, None)
                logger.debug("[LangGraphMemory] Checkpointer closed")
            except Exception as e:
                logger.warning(f"[LangGraphMemory] Error closing checkpointer | Error: {e!s}")

        if self._store_cm and self._store:
            try:
                await self._store_cm.__aexit__(None, None, None)
                logger.debug("[LangGraphMemory] Store closed")
            except Exception as e:
                logger.warning(f"[LangGraphMemory] Error closing store | Error: {e!s}")

        self._initialized = False
        self._checkpointer = None
        self._store = None
        self._checkpointer_cm = None
        self._store_cm = None

    def get_checkpointer(self) -> AsyncPostgresSaver | None:
        """
        Get the checkpointer instance.

        Returns:
            AsyncPostgresSaver if initialized and enabled, None otherwise
        """
        if not self.is_enabled or not self._initialized:
            return None
        return self._checkpointer

    def get_store(self) -> AsyncPostgresStore | None:
        """
        Get the store instance.

        Returns:
            AsyncPostgresStore if initialized and enabled, None otherwise
        """
        if not self.is_enabled or not self._initialized:
            return None
        return self._store

    def get_thread_id(
        self, conversation_id: str | None = None, user_id: str | None = None, chat_id: str | None = None
    ) -> str:
        """
        Generate thread_id from application IDs.

        Thread ID format: {user_id}:{conversation_id}
        This ensures each conversation has a unique thread while supporting multi-user scenarios.

        IMPORTANT: chat_id is intentionally NOT included because it changes per message.
        The thread_id must remain constant across all messages in a conversation.

        Args:
            conversation_id: Application conversation ID
            user_id: Application user ID
            chat_id: Application chat ID (not used in thread_id, only for fallback)

        Returns:
            Formatted thread ID string
        """
        # Use conversation_id as primary identifier, with fallbacks
        conv_id = conversation_id or "default"
        uid = user_id or "anonymous"

        thread_id = f"{uid}:{conv_id}"
        logger.debug(f"[LangGraphMemory] Thread ID generated | thread_id={thread_id}")

        return thread_id

    def trim_messages_if_enabled(self, messages: list[BaseMessage]) -> list[BaseMessage]:
        """
        Trim messages based on configuration to manage context window.

        Strategies:
        - Keep last N messages (configurable)
        - Token-based trimming (configurable max tokens)

        Args:
            messages: List of conversation messages

        Returns:
            Trimmed list of messages
        """
        if not settings.postgres.langgraph_message_trim_enabled:
            logger.debug("[LangGraphMemory] Message trimming disabled")
            return messages

        original_count = len(messages)

        try:
            # Strategy 1: Keep last N messages
            keep_last = settings.postgres.langgraph_message_trim_keep_last
            if keep_last > 0 and len(messages) > keep_last:
                # Always keep system message if present
                system_msgs = [m for m in messages if m.type == "system"]
                recent_msgs = messages[-keep_last:]

                # Combine system messages with recent messages
                trimmed = system_msgs + recent_msgs
                logger.info(
                    f"[LangGraphMemory] Messages trimmed | "
                    f"Original: {original_count} | Kept: {len(trimmed)} | "
                    f"Strategy: keep_last_{keep_last}"
                )
                return trimmed

            return messages

        except Exception as e:
            logger.warning(f"[LangGraphMemory] Message trimming failed | Error: {e!s}")
            return messages  # Return original on error

    def get_config(
        self,
        conversation_id: str | None = None,
        user_id: str | None = None,
        chat_id: str | None = None,
        additional_config: dict | None = None,
    ) -> dict:
        """
        Build LangGraph config with thread_id and checkpointer.

        Args:
            conversation_id: Application conversation ID
            user_id: Application user ID
            chat_id: Application chat ID
            additional_config: Additional config to merge

        Returns:
            LangGraph config dict ready for graph invocation
        """
        thread_id = self.get_thread_id(conversation_id, user_id, chat_id)

        config = {
            "configurable": {
                "thread_id": thread_id,
                "user_id": user_id or "anonymous",
                "conversation_id": conversation_id or "default",
                "chat_id": chat_id or "none",
            }
        }

        # Merge additional config if provided
        if additional_config:
            config.update(additional_config)

        logger.debug(f"[LangGraphMemory] Config built | thread_id={thread_id}")

        return config


# Singleton instance
_memory_manager: LangGraphMemory | None = None


def get_memory_manager() -> LangGraphMemory:
    """
    Get singleton memory manager instance.

    Returns:
        LangGraphMemory instance
    """
    global _memory_manager
    if _memory_manager is None:
        _memory_manager = LangGraphMemory()
    return _memory_manager


@asynccontextmanager
async def memory_lifespan():
    """
    Async context manager for memory lifecycle management.

    Usage:
        async with memory_lifespan():
            # Use memory system
            pass
    """
    memory = get_memory_manager()
    try:
        await memory.initialize()
        yield memory
    finally:
        await memory.close()
