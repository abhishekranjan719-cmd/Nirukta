"""
Common Pydantic schemas used across the application.
"""

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
