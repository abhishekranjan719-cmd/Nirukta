"""
QnA Workflow Router - Chain-based orchestration endpoints.
"""

from fastapi import APIRouter, HTTPException
from loguru import logger

from app.routers.qna_workflow.service import get_workflow_service
from app.schemas.qna import ProcessRequest, ProcessResponse


router = APIRouter(
    prefix="/api/v1/qna/workflow",
    tags=["qna", "workflow"],
)

# Get workflow service
workflow_service = get_workflow_service()


@router.post("/process", response_model=ProcessResponse)
async def process_workflow(request: ProcessRequest):
    """
    Process a message using chain-based workflow orchestration.

    This endpoint uses a simple sequential chain:
    1. Input validation
    2. LLM processing
    3. Response formatting

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
                f"Workflow request received | "
                f"User: {request.tracking.user_id} | "
                f"Chat: {request.tracking.chat_id} | "
                f"Conv: {request.tracking.conversation_id}"
            )
        else:
            logger.debug(f"Workflow request received | No tracking | Length: {len(request.message)}")

        # Process with workflow service (including conversation history)
        response_text, metadata = await workflow_service.process_question(
            message=request.message,
            context=request.context,
            tracking=request.tracking,
            conversation_history=request.conversation_history,
        )

        logger.info(
            f"Workflow request processed | "
            f"Response length: {len(response_text)} | "
            f"Chat ID: {request.tracking.chat_id if request.tracking else 'none'}"
        )

        return ProcessResponse(response=response_text, metadata=metadata, orchestration_mode="workflow")

    except ValueError as e:
        logger.warning(f"Workflow validation error | Error: {e!s}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception(f"Workflow processing error | Error: {e!s}")
        raise HTTPException(status_code=500, detail=f"Processing error: {e!s}")
