from langchain.chains import RetrievalQA
from langchain.llms import BaseLLM
from langchain_core.retrievers import BaseRetriever
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