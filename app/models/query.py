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