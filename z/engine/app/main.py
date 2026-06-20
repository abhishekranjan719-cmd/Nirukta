from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.config import settings
from app.routers.qna_agent import router as agent_router
from app.routers.qna_agent.memory import get_memory_manager
from app.routers.qna_agent.service import get_agent_service

# Import routers
from app.routers.qna_workflow import router as workflow_router
from app.routers.qna_workflow.service import get_workflow_service
from app.schemas import ProcessRequest, ProcessResponse
from app.services import MessageProcessor


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for FastAPI application.

    Manages lifecycle of async resources:
    - LangGraph memory system (PostgreSQL checkpointer and store)

    Startup:
    - Initialize memory manager with AsyncPostgresSaver and AsyncPostgresStore
    - Create database tables if they don't exist

    Shutdown:
    - Close database connections gracefully
    """
    # Startup: Initialize memory system
    memory = get_memory_manager()
    try:
        await memory.initialize()
        logger.info(
            "[Startup] LangGraph memory system initialized | "
            f"Enabled: {memory.is_enabled} | "
            f"Database: {settings.postgres.langgraph_db_name}"
        )
    except Exception as e:
        logger.warning(f"[Startup] Memory initialization failed (will continue without memory) | " f"Error: {e!s}")

    yield

    # Shutdown: Close connections
    try:
        await memory.close()
        logger.info("[Shutdown] LangGraph memory system closed")
    except Exception as e:
        logger.warning(f"[Shutdown] Error closing memory system | Error: {e!s}")


# Create FastAPI app with lifespan
app = FastAPI(
    title="Zuna Engine API",
    description="Message processing engine for Zuna",
    version="0.1.0",
    lifespan=lifespan,
)

# Configure CORS - IMPORTANT: Only allow requests from Backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,  # Only backend can access
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info(f"Engine API initialized | CORS origins: {settings.cors_origins}")
logger.info(f"Processor type: {settings.processor_type} | Mode: {settings.mode}")
logger.info(
    f"Memory system (Mem0): {'Enabled' if settings.memory.is_enabled else 'Disabled'} | Will be integrated in future"
)

# Register routers
app.include_router(workflow_router)
app.include_router(agent_router)
logger.info("Registered routers: workflow (/api/v1/qna/workflow), agent (/api/v1/qna/agent)")

# Initialize processor (for legacy endpoint)
processor = MessageProcessor()

# Initialize services
workflow_service = get_workflow_service()
agent_service = get_agent_service()


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "ok",
        "service": "engine",
        "timestamp": datetime.now().isoformat(),
    }


@app.post("/process", response_model=ProcessResponse)
async def process(request: ProcessRequest):
    """
    Process a message using LLM and return a response.

    This endpoint intelligently routes requests based on orchestration_mode:
    - orchestration_mode="workflow" (default): Uses chain-based sequential processing
    - orchestration_mode="agent": Uses agent-based autonomous processing

    Backend Integration:
    - LiteLLM proxy for LLM calls (GPT-4.1)
    - Langfuse for observability and tracing
    - Comprehensive tracking metadata for correlation

    Flow:
    1. Receive message, orchestration_mode, and tracking metadata from backend
    2. Route to appropriate service (workflow or agent)
    3. Create Langfuse trace with all tracking IDs
    4. Call LiteLLM proxy (GPT-4.1) for response
    5. Log LLM generation to Langfuse
    6. Return response with metadata and orchestration mode
    """
    try:
        # Log incoming request with tracking info
        if request.tracking:
            logger.info(
                f"Processing message [{request.orchestration_mode} mode] | "
                f"User: {request.tracking.user_id} | "
                f"Chat: {request.tracking.chat_id} | "
                f"Conv: {request.tracking.conversation_id} | "
                f"Usecase: {request.tracking.usecase_id}"
            )
        else:
            logger.debug(
                f"Processing message [{request.orchestration_mode} mode] | "
                f"No tracking | Length: {len(request.message)}"
            )

        # Route based on orchestration mode
        if request.orchestration_mode == "agent":
            # Use agent-based orchestration
            response_text, metadata = await agent_service.process_question(
                message=request.message,
                context=request.context,
                tracking=request.tracking,
                conversation_history=request.conversation_history,
            )
            orchestration_mode = "agent"
        else:
            # Use workflow (chain-based) orchestration (default)
            response_text, metadata = await workflow_service.process_question(
                message=request.message,
                context=request.context,
                tracking=request.tracking,
                conversation_history=request.conversation_history,
            )
            orchestration_mode = "workflow"

        logger.info(
            f"Message processed successfully [{orchestration_mode} mode] | "
            f"Response length: {len(response_text)} | "
            f"Chat ID: {request.tracking.chat_id if request.tracking else 'none'}"
        )

        return ProcessResponse(response=response_text, metadata=metadata, orchestration_mode=orchestration_mode)

    except ValueError as e:
        logger.warning(f"Validation error | Error: {e!s}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception(f"Processing error | Message: {e!s}")
        raise HTTPException(status_code=500, detail=f"Processing error: {e!s}")


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "service": "Zuna Engine",
        "version": "0.1.0",
        "description": "FastAPI-based message processing engine with multiple orchestration modes",
        "orchestration_modes": {
            "workflow": "Chain-based sequential processing (default)",
            "agent": "Agent-based autonomous processing with reasoning",
        },
        "endpoints": {
            "health": "/health",
            "process": "/process (supports orchestration_mode parameter)",
            "workflow_process": "/api/v1/qna/workflow/process",
            "agent_process": "/api/v1/qna/agent/process",
            "docs": "/docs",
            "redoc": "/redoc",
        },
        "note": "Use orchestration_mode='workflow' or 'agent' in the /process endpoint to choose processing mode",
    }
