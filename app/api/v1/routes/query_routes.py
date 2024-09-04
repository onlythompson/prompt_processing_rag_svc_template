from fastapi import APIRouter, Depends
from app.core.dependencies import get_query_controller
from app.api.v1.schemas.request.query_request import QueryRequest, ConversationRequest
from app.api.v1.schemas.response.query_response import QueryResponse, ConversationResponse
from app.api.v1.controllers.query_controller import QueryController

router = APIRouter()

@router.post("/query", response_model=QueryResponse)
async def process_query(
    query: QueryRequest,
    controller: QueryController = Depends(get_query_controller)
):
    return await controller.process_query(query)

@router.post("/conversation", response_model=ConversationResponse)
async def process_conversation(
    conversation: ConversationRequest,
    controller: QueryController = Depends(get_query_controller)
):
    return await controller.process_conversation(conversation)