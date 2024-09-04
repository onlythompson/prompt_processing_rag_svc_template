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