from pydantic import BaseModel

class UpdateKnowledgeBaseResponse(BaseModel):
    success: bool
    documents_processed: int

class SystemStatsResponse(BaseModel):
    total_documents: int
    total_queries_processed: int
    average_query_time: float