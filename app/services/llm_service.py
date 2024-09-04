from typing import List
from langchain_openai import ChatOpenAI
from app.core.config import Settings

class LLMService:
    def __init__(self):
        self.llm = None

    async def initialize(self, settings: Settings):
        self.llm = ChatOpenAI(
            temperature=settings.OPENAI_LLM_TEMPERATURE,
            model_name=settings.OPENAI_LLM_MODEL_NAME,
            max_tokens=settings.OPENAI_LLM_MAX_TOKENS,
            openai_api_key=settings.OPENAI_API_KEY
        )

    async def generate_text(self, prompt: str) -> str:
        if not self.llm:
            raise ValueError("LLMService not initialized. Call initialize() first.")
        return await self.llm.agenerate([prompt])

    async def get_embedding(self, text: str) -> List[float]:
        # This assumes you're using OpenAI's embedding model
        # You might need to use a different client or method depending on your setup
        if not self.llm:
            raise ValueError("LLMService not initialized. Call initialize() first.")
        
        embedding = await self.llm.embeddings.acreate(
            input=[text],
            model="text-embedding-ada-002",
            api_key=self.llm.openai_api_key
        )
        return embedding['data'][0]['embedding']