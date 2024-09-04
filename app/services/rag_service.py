from app.chains.rag_chain import RAGChain
from app.services.llm_service import LLMService
from app.services.retrieval_service import RetrievalService
from cross_cutting.compression import compress_prompt
from app.utils.prefiltering import preprocess_query
# from app.agents.react_agent import ReActAgent
from typing import Dict, Any

class RAGService:
    # def __init__(self):
    #     self.llm_service = None
    #     self.retrieval_service = None
    #     self.rag_chain = None
    #     self.react_agent = None

    def __init__(self, llm_service: LLMService, retrieval_service: RetrievalService):
        self.llm_service = llm_service
        self.retrieval_service = retrieval_service
        self.rag_chain = RAGChain(llm_service.llm, retrieval_service.retriever)
        # self.react_agent = ReActAgent(llm_service.llm)


    def initiialize(self, llm_service: LLMService, retrieval_service: RetrievalService):
        self.llm_service = llm_service
        self.retrieval_service = retrieval_service
        self.rag_chain = RAGChain(llm_service.llm, retrieval_service.retriever)
        # self.react_agent = ReActAgent(llm_service.llm)


    async def process_query(self, query: str) -> Dict[str, Any]:
        # Preprocess the query
        preprocessed_query = preprocess_query(query)
        
        # Compress the query
        compression_result = await compress_prompt(preprocessed_query)
        compressed_query = compression_result["compressed_prompt"]
        
        # Run the RAG chain with the compressed query
        result = await self.rag_chain.run(compressed_query)
        
        return {
            "answer": result["answer"],
            "sources": [doc.page_content for doc in result["source_documents"]],
            "query_compression": compression_result
        }
    
    # async def process_query_with_agents(self, query: str) -> Dict[str, Any]:
    #     # Preprocess the query
    #     preprocessed_query = preprocess_query(query)
        
    #     # Compress the query
    #     compression_result = await compress_prompt(preprocessed_query)
    #     compressed_query = compression_result["compressed_prompt"]
        
    #     # First, try to answer with the RAG chain
    #     rag_result = await self.rag_chain.run(compressed_query)
        
    #     # If the RAG chain couldn't find a good answer, use the ReAct agent
    #     if rag_result["answer"] == "I don't have enough information to answer this question.":
    #         agent_result = await self.react_agent.run(compressed_query)
    #         return {
    #             "answer": agent_result,
    #             "sources": [],  # The agent doesn't provide sources in the same way
    #             "query_compression": compression_result,
    #             "method": "agent"
    #         }
    #     else:
    #         return {
    #             "answer": rag_result["answer"],
    #             "sources": [doc.page_content for doc in rag_result["source_documents"]],
    #             "query_compression": compression_result,
    #             "method": "rag"
    #         }

    async def update_knowledge_base(self):
        new_retriever = await self.retrieval_service.get_updated_retriever()
        self.rag_chain.update_retriever(new_retriever)