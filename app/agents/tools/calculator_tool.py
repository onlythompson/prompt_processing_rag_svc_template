from langchain.tools import BaseTool
import numexpr

class CalculatorTool(BaseTool):
    name = "Calculator"
    description = "useful for when you need to perform mathematical calculations"

    async def _arun(self, query: str) -> str:
        try:
            result = numexpr.evaluate(query).item()
            return f"The result of the calculation is: {result}"
        except Exception as e:
            return f"Error in calculation: {str(e)}"