from fastapi import APIRouter, Depends
from app.api.v1.controllers.admin_controller import AdminController
from app.api.v1.schemas.response.admin_response import UpdateKnowledgeBaseResponse, SystemStatsResponse

router = APIRouter()

@router.post("/update-knowledge-base", response_model=UpdateKnowledgeBaseResponse)
async def update_knowledge_base(
    controller: AdminController = Depends()
):
    return await controller.update_knowledge_base()

@router.get("/system-stats", response_model=SystemStatsResponse)
async def get_system_stats(
    controller: AdminController = Depends()
):
    return await controller.get_system_stats()