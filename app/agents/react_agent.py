from langchain.agents import AgentType, initialize_agent
from langchain.llms import BaseLLM
from langchain.memory import ConversationBufferMemory
from app.agents.tools.search_tool import SearchTool
from app.agents.tools.calculator_tool import CalculatorTool

class ReActAgent:
    def __init__(self, llm: BaseLLM):
        self.llm = llm
        self.tools = [SearchTool(), CalculatorTool()]
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self.agent = initialize_agent(
            self.tools,
            self.llm,
            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
            memory=self.memory,
            verbose=True
        )

    async def run(self, query: str) -> str:
        response = await self.agent.arun(input=query)
        return response