"""
QnA Agent Router - Agent-based orchestration endpoints.
"""

from fastapi import APIRouter, HTTPException
from loguru import logger

from app.routers.qna_agent.service import get_agent_service
from app.schemas.qna import ProcessRequest, ProcessResponse


router = APIRouter(
    prefix="/api/v1/qna/agent",
    tags=["qna", "agent"],
)

# Get agent service
agent_service = get_agent_service()


@router.post("/process", response_model=ProcessResponse)
async def process_agent(request: ProcessRequest):
    """
    Process a message using agent-based orchestration.

    This endpoint uses an autonomous agent approach:
    1. Analyze question complexity
    2. Plan appropriate strategy
    3. Execute with reasoning
    4. Refine response if needed

    The agent can handle:
    - Simple factual questions
    - Complex multi-step reasoning
    - Explanatory queries
    - Open-ended discussions

    Args:
        request: ProcessRequest with message, context, and tracking

    Returns:
        ProcessResponse with answer and metadata

    Raises:
        HTTPException: If processing fails
    """
    try:
        # Log incoming request
        if request.tracking:
            logger.info(
                f"Agent request received | "
                f"User: {request.tracking.user_id} | "
                f"Chat: {request.tracking.chat_id} | "
                f"Conv: {request.tracking.conversation_id}"
            )
        else:
            logger.debug(f"Agent request received | No tracking | Length: {len(request.message)}")

        # Process with agent service (including conversation history)
        response_text, metadata = await agent_service.process_question(
            message=request.message,
            context=request.context,
            tracking=request.tracking,
            conversation_history=request.conversation_history,
        )

        logger.info(
            f"Agent request processed | "
            f"Response length: {len(response_text)} | "
            f"Chat ID: {request.tracking.chat_id if request.tracking else 'none'}"
        )

        return ProcessResponse(response=response_text, metadata=metadata, orchestration_mode="agent")

    except ValueError as e:
        logger.warning(f"Agent validation error | Error: {e!s}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception(f"Agent processing error | Error: {e!s}")
        raise HTTPException(status_code=500, detail=f"Processing error: {e!s}")
