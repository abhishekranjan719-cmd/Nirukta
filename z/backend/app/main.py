from datetime import datetime
from uuid import uuid4

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.config import settings
from app.models import ChatRequest, ChatResponse, Conversation, TrackingMetadata


# Create FastAPI app
app = FastAPI(
    title="Zuna Backend API",
    description="Backend API for Zuna",
    version="0.1.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info(f"Backend API initialized | CORS origins: {settings.cors_origins}")
logger.info(f"Engine URL: {settings.engine_url} | Mode: {settings.mode}")

# In-memory conversation storage
conversations: dict[str, Conversation] = {}


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "ok",
        "service": "backend",
        "timestamp": datetime.now().isoformat(),
    }


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint that receives messages from frontend and forwards to engine.

    Flow:
    1. Get or create conversation
    2. Generate tracking metadata with all IDs and aliases
    3. Add user message to conversation
    4. Forward message and tracking metadata to engine
    5. Add engine response to conversation
    6. Return response to frontend
    """
    try:
        # Get or create conversation
        conversation_id = request.conversation_id or str(uuid4())
        is_new = conversation_id not in conversations

        if is_new:
            conversations[conversation_id] = Conversation(conversation_id=conversation_id)
            logger.info(f"New conversation created | ID: {conversation_id}")

        conversation = conversations[conversation_id]

        # Generate comprehensive tracking metadata
        tracking = TrackingMetadata.create(
            user_id=request.user_id,  # Use provided user_id or generate
            chat_id=None,  # Always generate new chat_id for each message
            conversation_id=conversation_id,  # Use existing conversation_id
            usecase_id=request.usecase_id,  # Use provided usecase_id or generate
        )

        logger.info(
            f"Tracking metadata generated | "
            f"User: {tracking.user_id} | "
            f"Chat: {tracking.chat_id} | "
            f"Conv: {tracking.conversation_id} | "
            f"Usecase: {tracking.usecase_id}"
        )

        # Add user message
        conversation.add_message(role="user", content=request.message)
        logger.debug(f"User message added | Conv: {conversation_id} | Length: {len(request.message)}")

        # Forward to engine with tracking metadata and orchestration mode
        logger.debug(
            f"Forwarding to engine [{request.orchestration_mode} mode] | " f"URL: {settings.engine_url}/process"
        )
        async with httpx.AsyncClient(timeout=settings.engine_timeout) as client:
            try:
                engine_payload = {
                    "message": request.message,
                    "context": {},
                    "tracking": tracking.model_dump(),  # Send all tracking IDs and aliases
                    "orchestration_mode": request.orchestration_mode,  # Forward orchestration mode
                }

                engine_response = await client.post(
                    f"{settings.engine_url}/process",
                    json=engine_payload,
                )
                engine_response.raise_for_status()
                engine_data = engine_response.json()
                response_text = engine_data.get("response", "")
                orchestration_mode = engine_data.get("orchestration_mode", request.orchestration_mode)
                logger.info(
                    f"Engine response received [{orchestration_mode} mode] | "
                    f"Conv: {conversation_id} | "
                    f"Chat: {tracking.chat_id}"
                )
            except httpx.RequestError as e:
                logger.error(f"Engine connection failed | Error: {e!s}")
                raise HTTPException(
                    status_code=503,
                    detail=f"Failed to connect to engine: {e!s}",
                )
            except httpx.HTTPStatusError as e:
                logger.error(f"Engine returned error | Status: {e.response.status_code}")
                raise HTTPException(
                    status_code=e.response.status_code,
                    detail=f"Engine returned error: {e!s}",
                )

        # Add engine response to conversation
        conversation.add_message(role="assistant", content=response_text)
        logger.debug(f"Assistant message added | Conv: {conversation_id}")

        return ChatResponse(
            response=response_text,
            conversation_id=conversation_id,
            timestamp=datetime.now(),
            orchestration_mode=orchestration_mode,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Unexpected error in chat endpoint | Error: {e!s}")
        raise HTTPException(status_code=500, detail=f"Internal error: {e!s}")


@app.get("/api/conversations/{conversation_id}")
async def get_conversation(conversation_id: str):
    """Get conversation history by ID"""
    if conversation_id not in conversations:
        raise HTTPException(status_code=404, detail="Conversation not found")

    return conversations[conversation_id]


@app.get("/api/conversations")
async def list_conversations():
    """List all conversations"""
    return {
        "conversations": [
            {
                "conversation_id": conv.conversation_id,
                "message_count": len(conv.messages),
                "created_at": conv.created_at,
                "updated_at": conv.updated_at,
            }
            for conv in conversations.values()
        ]
    }
