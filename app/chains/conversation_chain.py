from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.llms import BaseLLM
from typing import Dict, Any

class RAGConversationChain:
    def __init__(self, llm: BaseLLM, memory: ConversationBufferMemory = None):
        self.memory = memory or ConversationBufferMemory()
        self.chain = ConversationChain(
            llm=llm,
            memory=self.memory,
            verbose=True
        )

    async def run(self, input_text: str) -> str:
        return await self.chain.arun(input_text)

    def load_memory_variables(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        return self.memory.load_memory_variables(inputs)

    def save_context(self, inputs: Dict[str, Any], outputs: Dict[str, str]) -> None:
        self.memory.save_context(inputs, outputs)

    def clear(self) -> None:
        self.memory.clear()