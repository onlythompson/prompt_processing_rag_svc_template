from fastapi import APIRouter
from .controllers import QueryController, AdminController
from .routes import query_routes, admin_routes
from .schemas.request import QueryRequest, ConversationRequest
from .schemas.response import QueryResponse, ConversationResponse, UpdateKnowledgeBaseResponse, SystemStatsResponse