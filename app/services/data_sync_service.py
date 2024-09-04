from app.db.mongodb import MongoDB
from app.services.llm_service import LLMService
from app.db.vector_store import VectorStore
from typing import List, Dict

class DataSyncService:
    def __init__(self):
        self.mongodb = None
        self.llm_service = None
        self.vector_store = None


    async def initialize(self, mongodb: MongoDB, llm_service: LLMService, vector_store: VectorStore):
        self.mongodb = mongodb
        self.llm_service = llm_service
        self.vector_store = vector_store

    async def sync_data(self):
        if not self.mongodb or not self.llm_service or not self.vector_store:
            raise ValueError("DataSyncService not initialized. Call initialize() first.")
        
        new_documents = await self.fetch_new_documents()
        processed_documents = await self.process_documents(new_documents)
        await self.update_vector_store(processed_documents)

    async def fetch_new_documents(self) -> List[Dict]:
        if not self.mongodb or not self.llm_service or not self.vector_store:
            raise ValueError("DataSyncService not initialized. Call initialize() first.")
        # Implement logic to fetch new documents from MongoDB
        return await self.mongodb.get_new_documents()

    async def process_documents(self, documents: List[Dict]) -> List[Dict]:
        if not self.mongodb or not self.llm_service or not self.vector_store:
            raise ValueError("DataSyncService not initialized. Call initialize() first.")
        
        processed_docs = []
        for doc in documents:
            embedding = await self.llm_service.get_embedding(doc['content'])
            processed_docs.append({
                'id': doc['_id'],
                'content': doc['content'],
                'embedding': embedding
            })
        return processed_docs

    async def update_vector_store(self, documents: List[Dict]):
        await self.vector_store.add_documents(documents)