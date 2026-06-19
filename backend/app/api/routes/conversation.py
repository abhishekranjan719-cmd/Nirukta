from fastapi import APIRouter

router = APIRouter()

# TODO: Implement conversation endpoints
@router.get("/")
async def conversation_root():
    return {"module": "conversation", "status": "scaffold"}
