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