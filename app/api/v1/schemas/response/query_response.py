from pydantic import BaseModel, Field
from typing import List

class Source(BaseModel):
    content: str
    metadata: dict

class CompressionInfo(BaseModel):
    original_tokens: int
    compressed_tokens: int
    compression_ratio: float

class QueryResponse(BaseModel):
    answer: str
    sources: List[Source]
    query_compression: CompressionInfo
    method: str = Field(..., description="Method used to generate the answer: 'rag' or 'agent'") #support rag or agent

class ConversationResponse(BaseModel):
    response: str
    conversation_id: str
    method: str = Field(..., description="Method used to generate the answer: 'rag' or 'agent'") #support rag or agent