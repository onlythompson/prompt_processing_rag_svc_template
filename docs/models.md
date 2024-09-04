## The `db` and `models` Directories. 

These contains database connections, vector store operations, and define the data models for your RAG-powered microservice.

Let's start with the implementations:

1. db/mongodb.py:



```python
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
from typing import List, Dict, Any

class MongoDB:
    def __init__(self):
        self.client = AsyncIOMotorClient(settings.MONGODB_URL)
        self.db = self.client[settings.MONGODB_DB_NAME]

    async def insert_document(self, collection: str, document: Dict[str, Any]) -> str:
        result = await self.db[collection].insert_one(document)
        return str(result.inserted_id)

    async def find_document(self, collection: str, query: Dict[str, Any]) -> Dict[str, Any]:
        return await self.db[collection].find_one(query)

    async def find_documents(self, collection: str, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        cursor = self.db[collection].find(query)
        return await cursor.to_list(length=None)

    async def update_document(self, collection: str, query: Dict[str, Any], update: Dict[str, Any]) -> int:
        result = await self.db[collection].update_one(query, {"$set": update})
        return result.modified_count

    async def delete_document(self, collection: str, query: Dict[str, Any]) -> int:
        result = await self.db[collection].delete_one(query)
        return result.deleted_count

    async def get_new_documents(self, collection: str, last_sync_time: float) -> List[Dict[str, Any]]:
        query = {"created_at": {"$gt": last_sync_time}}
        return await self.find_documents(collection, query)

```

2. db/vector_store.py:



```python
from typing import List, Dict, Any
import numpy as np
from fastapi import HTTPException
from langchain.vectorstores import FAISS
from langchain.docstore.document import Document
from langchain.embeddings import OpenAIEmbeddings
from app.core.config import settings

class VectorStore:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)
        self.vector_store = None

    async def initialize(self, documents: List[Dict[str, Any]]):
        docs = [Document(page_content=doc['content'], metadata=doc['metadata']) for doc in documents]
        self.vector_store = FAISS.from_documents(docs, self.embeddings)

    async def add_documents(self, documents: List[Dict[str, Any]]):
        if not self.vector_store:
            await self.initialize(documents)
        else:
            docs = [Document(page_content=doc['content'], metadata=doc['metadata']) for doc in documents]
            self.vector_store.add_documents(docs)

    async def similarity_search(self, query: str, k: int = 5) -> List[Document]:
        if not self.vector_store:
            raise HTTPException(status_code=500, detail="Vector store not initialized")
        docs = self.vector_store.similarity_search(query, k=k)
        return docs

    def as_retriever(self):
        if not self.vector_store:
            raise HTTPException(status_code=500, detail="Vector store not initialized")
        return self.vector_store.as_retriever()

    async def save(self, file_path: str):
        if not self.vector_store:
            raise HTTPException(status_code=500, detail="Vector store not initialized")
        self.vector_store.save_local(file_path)

    @classmethod
    async def load(cls, file_path: str):
        instance = cls()
        instance.vector_store = FAISS.load_local(file_path, instance.embeddings)
        return instance

```

Now, let's create the model implementations:

3. models/document.py:



```python
from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from datetime import datetime

class Document(BaseModel):
    id: str = Field(..., description="Unique identifier for the document")
    content: str = Field(..., description="The main text content of the document")
    metadata: Dict[str, str] = Field(default_factory=dict, description="Additional metadata about the document")
    embedding: Optional[List[float]] = Field(None, description="Vector embedding of the document")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of document creation")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of last update")

    class Config:
        schema_extra = {
            "example": {
                "id": "doc123",
                "content": "This is a sample document content.",
                "metadata": {"source": "web", "author": "John Doe"},
                "embedding": [0.1, 0.2, 0.3, 0.4],
                "created_at": "2023-06-01T12:00:00",
                "updated_at": "2023-06-01T12:00:00"
            }
        }

```

4. models/query.py:



```python
from pydantic import BaseModel, Field
from typing import Dict, Optional
from datetime import datetime

class Query(BaseModel):
    id: str = Field(..., description="Unique identifier for the query")
    text: str = Field(..., description="The text of the user's query")
    context: Dict[str, str] = Field(default_factory=dict, description="Additional context for the query")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of when the query was made")
    user_id: Optional[str] = Field(None, description="Identifier of the user who made the query")

    class Config:
        schema_extra = {
            "example": {
                "id": "query123",
                "text": "What is the capital of France?",
                "context": {"language": "en", "source": "web_interface"},
                "timestamp": "2023-06-01T12:00:00",
                "user_id": "user456"
            }
        }

```

5. models/response.py:



```python
from pydantic import BaseModel, Field
from typing import List, Dict
from datetime import datetime

class SourceDocument(BaseModel):
    id: str = Field(..., description="Identifier of the source document")
    content: str = Field(..., description="Relevant excerpt from the source document")
    metadata: Dict[str, str] = Field(default_factory=dict, description="Metadata of the source document")

class Response(BaseModel):
    id: str = Field(..., description="Unique identifier for the response")
    query_id: str = Field(..., description="Identifier of the corresponding query")
    answer: str = Field(..., description="The generated answer text")
    sources: List[SourceDocument] = Field(default_factory=list, description="List of source documents used")
    confidence: float = Field(..., ge=0, le=1, description="Confidence score of the answer")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of when the response was generated")

    class Config:
        schema_extra = {
            "example": {
                "id": "resp123",
                "query_id": "query123",
                "answer": "The capital of France is Paris.",
                "sources": [
                    {
                        "id": "doc456",
                        "content": "Paris is the capital and most populous city of France.",
                        "metadata": {"source": "wikipedia", "last_updated": "2023-05-01"}
                    }
                ],
                "confidence": 0.95,
                "timestamp": "2023-06-01T12:00:05"
            }
        }

```

These implementations provide a solid foundation for your RAG-powered microservice's data layer:

1. `mongodb.py`: Provides an async interface to MongoDB, handling basic CRUD operations and document retrieval.
2. `vector_store.py`: Implements a vector store using FAISS and LangChain, supporting document addition, similarity search, and persistence.
3. `document.py`: Defines the structure for documents in your system.
4. `query.py`: Represents user queries, including context and metadata.
5. `response.py`: Structures the system's responses, including answers, sources, and confidence scores.

To use these in your application:

1. Initialize the MongoDB and VectorStore in your FastAPI app's startup event:

```python
from fastapi import FastAPI
from app.db.mongodb import MongoDB
from app.db.vector_store import VectorStore

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    app.state.mongodb = MongoDB()
    app.state.vector_store = VectorStore()
    # Initialize vector store with documents from MongoDB
    documents = await app.state.mongodb.find_documents("documents", {})
    await app.state.vector_store.initialize(documents)

# In your API routes or services, you can access these like:
# mongodb = request.app.state.mongodb
# vector_store = request.app.state.vector_store
```

2. Use the models in your API schemas and database operations:

```python
from app.models.document import Document
from app.models.query import Query
from app.models.response import Response

@app.post("/documents")
async def create_document(document: Document):
    doc_id = await request.app.state.mongodb.insert_document("documents", document.dict())
    await request.app.state.vector_store.add_documents([document.dict()])
    return {"id": doc_id}

@app.post("/query")
async def process_query(query: Query):
    # Process the query using your RAG service
    # ...
    return Response(
        id="resp123",
        query_id=query.id,
        answer="Processed answer",
        sources=[],
        confidence=0.9
    )
```

Remember to handle exceptions, implement proper logging, and consider adding more sophisticated error handling, especially when dealing with database operations and the vector store.