"""
Health check router.
"""

from datetime import datetime

from fastapi import APIRouter


router = APIRouter(tags=["health"])


@router.get("/health")
async def health():
    """
    Health check endpoint.

    Returns basic service health information.
    """
    return {
        "status": "ok",
        "service": "engine",
        "timestamp": datetime.now().isoformat(),
    }


@router.get("/")
async def root():
    """
    Root endpoint with API information.
    """
    return {
        "service": "Zuna Engine",
        "version": "0.2.0",
        "endpoints": {
            "health": "/health",
            "process_workflow": "/api/v1/qna/workflow/process",
            "process_agent": "/api/v1/qna/agent/process",
            "docs": "/docs",
        },
    }
