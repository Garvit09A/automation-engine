from fastapi import APIRouter, Depends
from app.dependencies.auth import get_current_user

router = APIRouter()

@router.post("/")
async def create_workflow(
    name: str,
    current_user: str = Depends(get_current_user)
):
    return {
        "message": "Workflow created",
        "workflow_name": name,
        "owner": current_user
    }
