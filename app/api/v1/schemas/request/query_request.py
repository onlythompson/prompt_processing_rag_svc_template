from pydantic import BaseModel, Field

class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=1000)
    context: dict = Field(default={})

class ConversationRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)
    conversation_id: str = Field(default=None)