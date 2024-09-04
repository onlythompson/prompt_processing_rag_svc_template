from fastapi import Depends
from app.core.config import Settings
from app.db.mongodb import MongoDB
from app.db.vector_store import VectorStore
from app.services.llm_service import LLMService
from app.services.rag_service import RAGService
from app.services.retrieval_service import RetrievalService
from app.services.memory_service import MemoryService
from app.services.data_sync_service import DataSyncService
from app.services.summary_service import SummaryService
from app.agents.react_agent import ReActAgent
from app.agents.tools.search_tool import SearchTool
from app.agents.tools.calculator_tool import CalculatorTool

def get_settings():
    return Settings()

def get_mongodb(settings: Settings = Depends(get_settings))-> MongoDB:
    mongodb = MongoDB(url=settings.MONGODB_URL)
    return mongodb

def get_vector_store():
    return VectorStore()

def get_llm_service():
    return LLMService()

def get_retrieval_service(vector_store: VectorStore = Depends(get_vector_store)):
    return RetrievalService(vector_store)

def get_memory_service():
    return MemoryService()

def get_rag_service( llm_service: LLMService = Depends(get_llm_service),
    retrieval_service: RetrievalService = Depends(get_retrieval_service)):
    return RAGService(llm_service, retrieval_service)

# def get_data_sync_service(
#     mongodb: MongoDB = Depends(get_mongodb),
#     llm_service: LLMService = Depends(get_llm_service),
#     vector_store: VectorStore = Depends(get_vector_store)
# ):
#     # return DataSyncService(mongodb, llm_service, vector_store)
#     return DataSyncService()

def get_data_sync_service():
    # return DataSyncService(mongodb, llm_service, vector_store)
    return DataSyncService()

def get_summary_service(llm_service: LLMService = Depends(get_llm_service)):
    return SummaryService(llm_service)

def get_search_tool(rag_service: RAGService = Depends(get_rag_service)):
    return SearchTool(rag_service)

def get_calculator_tool():
    return CalculatorTool()

def get_react_agent(
    llm_service: LLMService = Depends(get_llm_service),
    search_tool: SearchTool = Depends(get_search_tool),
    calculator_tool: CalculatorTool = Depends(get_calculator_tool)
):
    return ReActAgent(llm_service.llm, [search_tool, calculator_tool])

def get_query_controller(
    rag_service: RAGService = Depends(get_rag_service),
    memory_service: MemoryService = Depends(get_memory_service)
):
    from app.api.v1.controllers.query_controller import QueryController
    return QueryController(rag_service, memory_service)

def get_admin_controller(
    data_sync_service: DataSyncService = Depends(get_data_sync_service)
):
    from app.api.v1.controllers.admin_controller import AdminController
    return AdminController(data_sync_service)