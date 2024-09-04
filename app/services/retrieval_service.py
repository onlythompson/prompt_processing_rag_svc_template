from app.db.vector_store import VectorStore
from typing import List, Dict
from langchain_core.retrievers import BaseRetriever

class RetrievalService:
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store
        self.retriever = self.vector_store.as_retriever()

    async def retrieve_documents(self, query: str, k: int = 5) -> List[Dict]:
        docs = await self.retriever.aget_relevant_documents(query)
        return [{'content': doc.page_content, 'metadata': doc.metadata} for doc in docs[:k]]

    async def get_updated_retriever(self) -> BaseRetriever:
        # This method would be called if the vector store has been updated
        return self.vector_store.as_retriever()