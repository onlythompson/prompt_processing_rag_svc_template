from langchain.memory import ConversationBufferMemory
from typing import Dict, Any

class MemoryService:
    def __init__(self):
        self.memories = {}

    def get_memory(self, conversation_id: str) -> ConversationBufferMemory:
        if conversation_id not in self.memories:
            self.memories[conversation_id] = ConversationBufferMemory()
        return self.memories[conversation_id]

    def save_context(self, conversation_id: str, inputs: Dict[str, Any], outputs: Dict[str, str]):
        memory = self.get_memory(conversation_id)
        memory.save_context(inputs, outputs)

    def load_memory_variables(self, conversation_id: str) -> Dict[str, Any]:
        memory = self.get_memory(conversation_id)
        return memory.load_memory_variables({})

    def clear_memory(self, conversation_id: str):
        if conversation_id in self.memories:
            del self.memories[conversation_id]