from typing import List, Dict, Any
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

class VectorStore:
    def __init__(self):
        self.vector_store = None
        self.embeddings = None

    async def initialize(self, documents: List[Dict[str, Any]], openai_api_key: str):
        self.embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
        docs = [Document(page_content=doc['content'], metadata=doc['metadata']) for doc in documents]

        if docs:
            self.vector_store = FAISS.from_documents(docs, self.embeddings)

    async def add_documents(self, documents: List[Dict[str, Any]]):
        if not self.vector_store:
            raise ValueError("VectorStore not initialized. Call initialize() first.")
        docs = [Document(page_content=doc['content'], metadata=doc['metadata']) for doc in documents]
        self.vector_store.add_documents(docs)

    async def similarity_search(self, query: str, k: int = 5) -> List[Document]:
        if not self.vector_store:
            raise ValueError("VectorStore not initialized. Call initialize() first.")
        docs = self.vector_store.similarity_search(query, k=k)
        return docs

    def as_retriever(self):
        if not self.vector_store:
            raise ValueError("VectorStore not initialized. Call initialize() first.")
        return self.vector_store.as_retriever()

    async def save(self, file_path: str):
        if not self.vector_store:
            raise ValueError("VectorStore not initialized. Call initialize() first.")
        self.vector_store.save_local(file_path)

    @classmethod
    async def load(cls, file_path: str, openai_api_key: str):
        instance = cls()
        instance.embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
        instance.vector_store = FAISS.load_local(file_path, instance.embeddings)
        return instance