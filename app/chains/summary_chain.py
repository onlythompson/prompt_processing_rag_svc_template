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