## Chains

This contains the LangChain components for your RAG-powered microservice. We'll implement three main chain types: conversation chain, summary chain, and RAG chain.

Let's start with the implementations:

1. conversation_chain.py:



```python
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

```

2. summary_chain.py:



```python
from langchain.chains.summarize import load_summarize_chain
from langchain.llms import BaseLLM
from langchain.docstore.document import Document
from typing import List

class RAGSummaryChain:
    def __init__(self, llm: BaseLLM, chain_type: str = "map_reduce"):
        self.chain = load_summarize_chain(llm, chain_type=chain_type)

    async def run(self, documents: List[Document]) -> str:
        return await self.chain.arun(documents)

    @staticmethod
    def create_documents(texts: List[str]) -> List[Document]:
        return [Document(page_content=text) for text in texts]

```

3. rag_chain.py:



```python
from langchain.chains import RetrievalQA
from langchain.llms import BaseLLM
from langchain.retrievers import BaseRetriever
from langchain.prompts import PromptTemplate
from typing import Dict, Any, Optional

class RAGChain:
    def __init__(
        self,
        llm: BaseLLM,
        retriever: BaseRetriever,
        prompt_template: Optional[str] = None
    ):
        if prompt_template:
            prompt = PromptTemplate(
                template=prompt_template,
                input_variables=["context", "question"]
            )
        else:
            prompt = None

        self.chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": prompt} if prompt else {}
        )

    async def run(self, query: str) -> Dict[str, Any]:
        result = await self.chain({"query": query})
        return {
            "answer": result["result"],
            "source_documents": result["source_documents"]
        }

    def update_retriever(self, new_retriever: BaseRetriever) -> None:
        self.chain.retriever = new_retriever

```

These implementations provide a solid foundation for the chain components of your RAG-powered microservice:

1. `RAGConversationChain`:
   - Maintains conversation context using LangChain's ConversationChain.
   - Allows for saving and loading memory variables.
   - Provides methods to run the conversation, save context, and clear memory.

2. `RAGSummaryChain`:
   - Implements document summarization using LangChain's summarization chain.
   - Supports different summarization strategies (e.g., map_reduce).
   - Includes a utility method to create Document objects from text strings.

3. `RAGChain`:
   - Implements the core RAG functionality using LangChain's RetrievalQA chain.
   - Supports custom prompt templates for more control over the generation process.
   - Returns both the generated answer and the source documents used.
   - Allows for updating the retriever, which can be useful for dynamic knowledge bases.

To use these in your application:

1. First, ensure you have LangChain and its dependencies installed:
   ```
   pip install langchain openai faiss-cpu
   ```

2. You can then use these chains in your service layer. For example:

   ```python
   from app.chains.rag_chain import RAGChain
   from langchain.llms import OpenAI
   from langchain.retrievers import FAISSRetriever

   class RAGService:
       def __init__(self, retriever: FAISSRetriever):
           llm = OpenAI(temperature=0.7)
           self.rag_chain = RAGChain(llm, retriever)

       async def process_query(self, query: str):
           result = await self.rag_chain.run(query)
           return result
   ```

3. For conversation management:

   ```python
   from app.chains.conversation_chain import RAGConversationChain
   from langchain.llms import OpenAI
   from langchain.memory import ConversationBufferMemory

   class ConversationService:
       def __init__(self):
           llm = OpenAI(temperature=0.7)
           memory = ConversationBufferMemory()
           self.conversation_chain = RAGConversationChain(llm, memory)

       async def process_message(self, message: str):
           response = await self.conversation_chain.run(message)
           return response
   ```

4. For summarization:

   ```python
   from app.chains.summary_chain import RAGSummaryChain
   from langchain.llms import OpenAI

   class SummaryService:
       def __init__(self):
           llm = OpenAI(temperature=0.3)
           self.summary_chain = RAGSummaryChain(llm)

       async def summarize_texts(self, texts: List[str]):
           documents = self.summary_chain.create_documents(texts)
           summary = await self.summary_chain.run(documents)
           return summary
   ```

Remember to handle exceptions, implement proper logging, and consider adding more sophisticated error handling and retrying mechanisms, especially when dealing with external LLM APIs.

Also, ensure that you're following best practices for API key management and not hardcoding sensitive information.



## Services

This contains the core services for your RAG-powered microservice. We'll implement services for RAG operations, LLM interactions, data synchronization, memory management, summarization, and retrieval.

Let's start with the implementations:

1. rag_service.py:



```python
from app.chains.rag_chain import RAGChain
from app.services.llm_service import LLMService
from app.services.retrieval_service import RetrievalService
from cross_cutting.compression import compress_prompt
from app.utils.prefiltering import preprocess_query
from typing import Dict, Any

class RAGService:
    def __init__(self, llm_service: LLMService, retrieval_service: RetrievalService):
        self.llm_service = llm_service
        self.retrieval_service = retrieval_service
        self.rag_chain = RAGChain(llm_service.llm, retrieval_service.retriever)

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

    async def update_knowledge_base(self):
        new_retriever = await self.retrieval_service.get_updated_retriever()
        self.rag_chain.update_retriever(new_retriever)
```

2. llm_service.py:



```python
from langchain.llms import OpenAI
from app.core.config import settings

class LLMService:
    def __init__(self):
        self.llm = OpenAI(
            temperature=settings.LLM_TEMPERATURE,
            model_name=settings.LLM_MODEL_NAME,
            max_tokens=settings.LLM_MAX_TOKENS
        )

    async def generate_text(self, prompt: str) -> str:
        return await self.llm.agenerate([prompt])

    async def get_embedding(self, text: str) -> List[float]:
        # This assumes you're using OpenAI's embedding model
        # You might need to use a different client or method depending on your setup
        embedding = await openai.Embedding.acreate(
            input=[text],
            model=settings.EMBEDDING_MODEL_NAME
        )
        return embedding['data'][0]['embedding']

```

3. data_sync_service.py:



```python
from app.db.mongodb import MongoDB
from app.services.llm_service import LLMService
from app.db.vector_store import VectorStore
from typing import List, Dict

class DataSyncService:
    def __init__(self, mongodb: MongoDB, llm_service: LLMService, vector_store: VectorStore):
        self.mongodb = mongodb
        self.llm_service = llm_service
        self.vector_store = vector_store

    async def sync_data(self):
        new_documents = await self.fetch_new_documents()
        processed_documents = await self.process_documents(new_documents)
        await self.update_vector_store(processed_documents)

    async def fetch_new_documents(self) -> List[Dict]:
        # Implement logic to fetch new documents from MongoDB
        return await self.mongodb.get_new_documents()

    async def process_documents(self, documents: List[Dict]) -> List[Dict]:
        processed_docs = []
        for doc in documents:
            embedding = await self.llm_service.get_embedding(doc['content'])
            processed_docs.append({
                'id': doc['_id'],
                'content': doc['content'],
                'embedding': embedding
            })
        return processed_docs

    async def update_vector_store(self, documents: List[Dict]):
        await self.vector_store.add_documents(documents)

```

4. memory_service.py:



```python
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

```

5. summary_service.py:



```python
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

```

6. retrieval_service.py:



```python
from app.db.vector_store import VectorStore
from langchain.retrievers import BaseRetriever
from typing import List, Dict

class RetrievalService:
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store
        self.retriever = self.vector_store.as_retriever()

    async def retrieve_documents(self, query: str, k: int = 5) -> List[Dict]:
        docs = await self.retriever.aget_relevant_documents(query)
        return [{'content': doc.page_content, 'metadata': doc.metadata} for doc in docs[:k]]

    async def get_updated_retriever(self) -> BaseRetriever:
        # This method would be called if the vector store has been updated
        return self.vector_store.as_retriever()

```

These implementations provide a comprehensive set of services for your RAG-powered microservice:

1. `RAGService`: Orchestrates the RAG process, integrating the LLM and retrieval services.
2. `LLMService`: Manages interactions with the language model, including text generation and embedding creation.
3. `DataSyncService`: Handles synchronization between your main database and the vector store.
4. `MemoryService`: Manages conversation memory for maintaining context in multi-turn interactions.
5. `SummaryService`: Provides text summarization capabilities for documents and conversations.
6. `RetrievalService`: Manages document retrieval operations using the vector store.

To use these services in your application:

1. You'll need to set up dependency injection in your FastAPI app. Here's an example of how you might set this up:

```python
from fastapi import FastAPI, Depends
from app.services.rag_service import RAGService
from app.services.llm_service import LLMService
from app.services.retrieval_service import RetrievalService
from app.services.data_sync_service import DataSyncService
from app.services.memory_service import MemoryService
from app.services.summary_service import SummaryService
from app.db.mongodb import MongoDB
from app.db.vector_store import VectorStore

app = FastAPI()

def get_mongodb():
    return MongoDB()

def get_vector_store():
    return VectorStore()

def get_llm_service():
    return LLMService()

def get_retrieval_service(vector_store: VectorStore = Depends(get_vector_store)):
    return RetrievalService(vector_store)

def get_rag_service(
    llm_service: LLMService = Depends(get_llm_service),
    retrieval_service: RetrievalService = Depends(get_retrieval_service)
):
    return RAGService(llm_service, retrieval_service)

def get_data_sync_service(
    mongodb: MongoDB = Depends(get_mongodb),
    llm_service: LLMService = Depends(get_llm_service),
    vector_store: VectorStore = Depends(get_vector_store)
):
    return DataSyncService(mongodb, llm_service, vector_store)

def get_memory_service():
    return MemoryService()

def get_summary_service(llm_service: LLMService = Depends(get_llm_service)):
    return SummaryService(llm_service)

@app.post("/query")
async def process_query(
    query: str,
    rag_service: RAGService = Depends(get_rag_service)
):
    result = await rag_service.process_query(query)
    return {
        "answer": result["answer"],
        "sources": result["sources"],
        "query_compression": {
            "original_tokens": result["query_compression"]["original_tokens"],
            "compressed_tokens": result["query_compression"]["compressed_tokens"],
            "compression_ratio": result["query_compression"]["compression_ratio"]
        }
    }

@app.post("/summarize")
async def summarize_texts(
    texts: List[str],
    summary_service: SummaryService = Depends(get_summary_service)
):
    summary = await summary_service.summarize_texts(texts)
    return {"summary": summary}

# Add more endpoints as needed
```

Remember to handle exceptions, implement proper logging, and consider adding more sophisticated error handling and retrying mechanisms, especially when dealing with external services and databases.

Also, ensure that you're following best practices for configuration management and not hardcoding sensitive information.
