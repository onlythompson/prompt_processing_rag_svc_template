from langchain.tools import BaseTool
from app.services.rag_service import RAGService

class SearchTool(BaseTool):
    name = "Search"
    description = "useful for when you need to answer questions about current events or the current state of the world"

    def __init__(self, rag_service: RAGService):
        super().__init__()
        self.rag_service = rag_service

    async def _arun(self, query: str) -> str:
        result = await self.rag_service.process_query(query)
        return result['answer']