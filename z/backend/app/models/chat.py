from datetime import datetime
from typing import Literal
from uuid import uuid4

from pydantic import BaseModel, Field


class TrackingMetadata(BaseModel):
    """
    Comprehensive tracking metadata for observability and tracing.

    Primary IDs:
    - user_id: User identifier
    - chat_id: Individual request/message identifier
    - conversation_id: Conversation/session identifier
    - usecase_id: Use case/application identifier

    Aliases for compatibility with different systems:
    - chat_id aliases: request_id, run_id, correlation_id, observation_id
    - conversation_id aliases: session_id, thread_id
    - usecase_id aliases: app_id, agent_id
    - user_id alias: user_email
    """

    # Primary IDs
    user_id: str = Field(..., description="User identifier")
    chat_id: str = Field(..., description="Individual chat/request identifier")
    conversation_id: str = Field(..., description="Conversation/session identifier")
    usecase_id: str = Field(..., description="Use case/application identifier")

    # chat_id aliases
    request_id: str = Field(..., description="Alias for chat_id - request identifier")
    run_id: str = Field(..., description="Alias for chat_id - run identifier")
    correlation_id: str = Field(..., description="Alias for chat_id - correlation identifier")
    observation_id: str = Field(..., description="Alias for chat_id - observation identifier")

    # conversation_id aliases
    session_id: str = Field(..., description="Alias for conversation_id - session identifier")
    thread_id: str = Field(..., description="Alias for conversation_id - thread identifier")

    # usecase_id aliases
    app_id: str = Field(..., description="Alias for usecase_id - application identifier")
    agent_id: str = Field(..., description="Alias for usecase_id - agent identifier")

    # user_id alias
    user_email: str = Field(..., description="Alias for user_id - user email")

    @classmethod
    def create(
        cls,
        user_id: str | None = None,
        chat_id: str | None = None,
        conversation_id: str | None = None,
        usecase_id: str | None = None,
    ) -> "TrackingMetadata":
        """
        Create TrackingMetadata with auto-generated UUIDs and aliases.

        Args:
            user_id: User identifier (generates UUID if None)
            chat_id: Chat identifier (generates UUID if None)
            conversation_id: Conversation identifier (generates UUID if None)
            usecase_id: Use case identifier (generates UUID if None)

        Returns:
            TrackingMetadata instance with all IDs and aliases populated
        """
        # Generate UUIDs if not provided
        user_id = user_id or str(uuid4())
        chat_id = chat_id or str(uuid4())
        conversation_id = conversation_id or str(uuid4())
        usecase_id = usecase_id or str(uuid4())

        return cls(
            # Primary IDs
            user_id=user_id,
            chat_id=chat_id,
            conversation_id=conversation_id,
            usecase_id=usecase_id,
            # chat_id aliases (all same as chat_id)
            request_id=chat_id,
            run_id=chat_id,
            correlation_id=chat_id,
            observation_id=chat_id,
            # conversation_id aliases (all same as conversation_id)
            session_id=conversation_id,
            thread_id=conversation_id,
            # usecase_id aliases (all same as usecase_id)
            app_id=usecase_id,
            agent_id=usecase_id,
            # user_id alias (same as user_id for now, could be actual email)
            user_email=user_id,
        )


class ChatRequest(BaseModel):
    """Request model for chat endpoint"""

    message: str = Field(..., min_length=1, description="The user's message")
    conversation_id: str | None = Field(None, description="Optional conversation ID to continue existing conversation")
    user_id: str | None = Field(None, description="Optional user ID for tracking")
    usecase_id: str | None = Field(None, description="Optional use case ID for tracking")
    orchestration_mode: Literal["workflow", "agent"] = Field(
        default="workflow", description="Orchestration mode: 'workflow' for chain-based, 'agent' for agent-based"
    )


class ChatResponse(BaseModel):
    """Response model for chat endpoint"""

    response: str = Field(..., description="The engine's response")
    conversation_id: str = Field(..., description="The conversation ID")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")
    orchestration_mode: str = Field(..., description="The orchestration mode used for processing")


class Message(BaseModel):
    """Individual message in a conversation"""

    role: str = Field(..., description="Message role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")
    timestamp: datetime = Field(default_factory=datetime.now, description="Message timestamp")


class Conversation(BaseModel):
    """Conversation containing multiple messages"""

    conversation_id: str = Field(default_factory=lambda: str(uuid4()), description="Unique conversation ID")
    messages: list[Message] = Field(default_factory=list, description="List of messages in the conversation")
    created_at: datetime = Field(default_factory=datetime.now, description="Conversation creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update timestamp")

    def add_message(self, role: str, content: str) -> None:
        """Add a message to the conversation"""
        self.messages.append(Message(role=role, content=content))
        self.updated_at = datetime.now()
