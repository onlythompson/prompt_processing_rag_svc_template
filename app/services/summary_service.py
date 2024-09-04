from app.chains.summary_chain import RAGSummaryChain
from app.services.llm_service import LLMService
from typing import List

class SummaryService:
    def __init__(self, llm_service: LLMService):
        self.summary_chain = RAGSummaryChain(llm_service.llm)

    async def summarize_texts(self, texts: List[str]) -> str:
        documents = self.summary_chain.create_documents(texts)
        summary = await self.summary_chain.run(documents)
        return summary

    async def summarize_conversation(self, conversation_history: List[str]) -> str:
        # Join the conversation history into a single string
        full_conversation = "\n".join(conversation_history)
        documents = self.summary_chain.create_documents([full_conversation])
        summary = await self.summary_chain.run(documents)
        return summary