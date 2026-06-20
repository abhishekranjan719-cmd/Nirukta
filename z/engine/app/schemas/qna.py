"""
QnA-specific Pydantic schemas for request/response models.
"""

from typing import Literal

from pydantic import BaseModel, Field

from app.schemas.common import TrackingMetadata


class ProcessRequest(BaseModel):
    """
    Request model for QnA processing endpoint.

    Supports both workflow (chain-based) and agent-based orchestration.
    Multi-turn conversation support via conversation_history.
    """

    message: str = Field(..., min_length=1, description="The message to process")
    context: dict | None = Field(None, description="Optional context for processing")
    tracking: TrackingMetadata | None = Field(None, description="Tracking metadata for observability")
    conversation_history: list[dict[str, str]] | None = Field(
        default=None,
        description="Previous conversation messages in OpenAI format: [{'role': 'user'/'assistant', 'content': '...'}]",
    )
    orchestration_mode: Literal["workflow", "agent"] = Field(
        default="workflow", description="Orchestration mode: 'workflow' for chain-based, 'agent' for agent-based"
    )


class ProcessResponse(BaseModel):
    """Response model for QnA processing endpoint"""

    response: str = Field(..., description="The processed response")
    metadata: dict = Field(default_factory=dict, description="Additional metadata about the processing")
    orchestration_mode: str = Field(..., description="The orchestration mode used for processing")
