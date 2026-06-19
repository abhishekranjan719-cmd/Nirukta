from fastapi import APIRouter

router = APIRouter()

# TODO: Implement auth endpoints
@router.get("/")
async def auth_root():
    return {"module": "auth", "status": "scaffold"}
