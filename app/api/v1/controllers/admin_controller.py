# from app.core.dependencies import get_llm_service
from app.core.dependencies import get_data_sync_service
from app.services.data_sync_service import DataSyncService
from app.api.v1.schemas.response.admin_response import UpdateKnowledgeBaseResponse, SystemStatsResponse
from fastapi import Depends


class AdminController:
    def __init__(self, data_sync_service: DataSyncService = Depends(get_data_sync_service)):
        self.data_sync_service = data_sync_service

    async def update_knowledge_base(self) -> UpdateKnowledgeBaseResponse:
        result = await self.data_sync_service.sync_data()
        return UpdateKnowledgeBaseResponse(
            success=result["success"],
            documents_processed=result["documents_processed"]
        )

    async def get_system_stats(self) -> SystemStatsResponse:
        # This would typically involve gathering stats from various services
        # For now, we'll return mock data
        return SystemStatsResponse(
            total_documents=1000,
            total_queries_processed=5000,
            average_query_time=0.5
        )