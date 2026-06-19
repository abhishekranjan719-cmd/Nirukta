from fastapi import APIRouter

router = APIRouter()

# TODO: Implement evaluation endpoints
@router.get("/")
async def evaluation_root():
    return {"module": "evaluation", "status": "scaffold"}
