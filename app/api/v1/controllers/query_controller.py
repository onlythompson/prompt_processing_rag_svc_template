from app.services.rag_service import RAGService
from app.services.memory_service import MemoryService
from app.api.v1.schemas.request.query_request import QueryRequest, ConversationRequest
from app.api.v1.schemas.response.query_response import QueryResponse, ConversationResponse, Source, CompressionInfo

class QueryController:
    def __init__(self, rag_service: RAGService, memory_service: MemoryService):
        self.rag_service = rag_service
        self.memory_service = memory_service

    async def process_query(self, query: QueryRequest) -> QueryResponse:
        result = await self.rag_service.process_query(query.query)
        return QueryResponse(
            answer=result["answer"],
            sources=[Source(content=source, metadata={}) for source in result["sources"]],
            query_compression=CompressionInfo(**result["query_compression"])
        )
    
    async def process_query_with_agents(self, query: QueryRequest) -> QueryResponse:
        result = await self.rag_service.process_query(query.query)
        return QueryResponse(
            answer=result["answer"],
            sources=[Source(content=source, metadata={}) for source in result.get("sources", [])],
            query_compression=CompressionInfo(**result["query_compression"]),
            method=result["method"]
        )

    async def process_conversation_with_agents(self, conversation: ConversationRequest) -> ConversationResponse:
        memory = self.memory_service.get_memory(conversation.conversation_id)
        context = memory.load_memory_variables({})
        
        result = await self.rag_service.process_query(conversation.message, context=context)
        
        memory.save_context({"input": conversation.message}, {"output": result["answer"]})
        
        return ConversationResponse(
            response=result["answer"],
            conversation_id=conversation.conversation_id or "new_conversation_id",  # Generate a new ID if not provided
            method=result["method"]
        )

    async def process_conversation(self, conversation: ConversationRequest) -> ConversationResponse:
        memory = self.memory_service.get_memory(conversation.conversation_id)
        context = memory.load_memory_variables({})
        
        result = await self.rag_service.process_query(conversation.message, context=context)
        
        memory.save_context({"input": conversation.message}, {"output": result["answer"]})
        
        return ConversationResponse(
            response=result["answer"],
            conversation_id=conversation.conversation_id or "new_conversation_id"  # Generate a new ID if not provided
        )