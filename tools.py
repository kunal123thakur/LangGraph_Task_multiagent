

from langchain.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults

@tool
def calculator_tool(input: str) -> str:
    """Solve basic math expressions. Input should be a math string like '2+2'."""
    try:
        result = eval(input)
        return str(result)
    except Exception as e:
        return f"Calculator Error: {str(e)}"

@tool
def webscraper_tool(url: str) -> str:
    """Simulate web scraping for a URL."""
    return f"Simulated content from {url}"

@tool
def mock_tool(input: str) -> str:
    """Mock tool for testing purposes. Just echoes the input."""
    return f"Mock response for: {input}"

@tool
def transfer_to_tools_Agent():
    """Ask tool_Agent for help."""
    return

@tool
def transfer_to_plan_Agent():
    """Ask plan_Agent for help."""
    return

@tool
def search(query: str) -> str:
    """Perform the web search on the user query."""
    tavily = TavilySearchResults()
    result = tavily.invoke(query)
    return result
