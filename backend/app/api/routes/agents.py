from fastapi import APIRouter

router = APIRouter()

# TODO: Implement agents endpoints
@router.get("/")
async def agents_root():
    return {"module": "agents", "status": "scaffold"}
