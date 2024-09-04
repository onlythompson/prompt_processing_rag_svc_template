# from llmlingua import PromptCompressor
from langchain_community.document_compressors import LLMLinguaCompressor
from functools import wraps
from typing import Callable, Any
import asyncio
from pydantic import BaseModel


# from langchain.retrievers import ContextualCompressionRetriever
# from langchain_community.document_compressors import LLMLinguaCompressor
# from langchain_openai import ChatOpenAI

# llm = ChatOpenAI(temperature=0)

# embedding = OpenAIEmbeddings(model="text-embedding-ada-002")
# retriever = FAISS.from_documents(texts, embedding).as_retriever(search_kwargs={"k": 20})

# compressor = LLMLinguaCompressor(model_name="openai-community/gpt2", device_map="cpu")
# compression_retriever = ContextualCompressionRetriever(
#     base_compressor=compressor, base_retriever=retriever
# )
# compressed_docs = compression_retriever.invoke(
#     "What did the president say about Ketanji Jackson Brown"
# )

class CompressionResult(BaseModel):
    original_prompt: str
    compressed_prompt: str
    original_tokens: int
    compressed_tokens: int
    compression_ratio: float

class LLMCompressor:
    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        # self.compressor = PromptCompressor(model_name=model_name)
        
        self.compressor = LLMLinguaCompressor(model_name="openai-community/gpt2", device_map="cpu")
    
    async def compress(self, prompt: str, ratio: float = 0.5) -> CompressionResult:
        loop = asyncio.get_event_loop()
        compressed_prompt = await loop.run_in_executor(
            None, self.compressor.compress_prompt, prompt, ratio
        )
        
        original_tokens = len(prompt.split())
        compressed_tokens = len(compressed_prompt.split())
        compression_ratio = 1 - (compressed_tokens / original_tokens)
        
        return CompressionResult(
            original_prompt=prompt,
            compressed_prompt=compressed_prompt,
            original_tokens=original_tokens,
            compressed_tokens=compressed_tokens,
            compression_ratio=compression_ratio
        )

def compress_prompt(ratio: float = 0.5):
    compressor = LLMCompressor()
    
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if 'prompt' in kwargs:
                compression_result = await compressor.compress(kwargs['prompt'], ratio)
                kwargs['prompt'] = compression_result.compressed_prompt
                kwargs['compression_result'] = compression_result
            return await func(*args, **kwargs)
        return wrapper
    
    return decorator

# Example usage
# @compress_prompt(ratio=0.6)
# async def process_query(prompt: str, compression_result: CompressionResult = None):
#     # Your query processing logic here
#     print(f"Processing compressed prompt: {prompt}")
#     if compression_result:
#         print(f"Compression ratio: {compression_result.compression_ratio:.2%}")
#     # ... rest of the processing logic

# # Utility function for manual compression
# async def manual_compress(prompt: str, ratio: float = 0.5) -> CompressionResult:
#     compressor = LLMCompressor()
#     return await compressor.compress(prompt, ratio)