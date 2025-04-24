
from langchain_core.messages import HumanMessage
from langchain.agents import initialize_agent, AgentType, Tool
from tools import calculator_tool, webscraper_tool, mock_tool, search
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()
GROK_API_KEY = os.getenv("GROK_API_KEY")
llm = ChatGroq(api_key=GROK_API_KEY, model_name="Gemma2-9b-It")

tools = [
    Tool.from_function(func=calculator_tool, name="Calculator", description="Useful for performing basic math operations"),
    Tool.from_function(func=webscraper_tool, name="WebScraper", description="Useful for answering questions by scraping the web"),
    Tool.from_function(func=mock_tool, name="MockTool", description="A mock tool for testing purposes"),
    Tool.from_function(func=search, name="Search", description="Perform a web search on the user query")
]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

def plan_agent_fn(state):
    """
    Plans tasks iteratively based on input. It adds, deletes, or modifies tasks.
    """
    query = state['input']
    history = state.get("history", [])
    prompt = f"""
You are a planning agent. Your job is to break down the user input into clear steps (tasks).
Make sure to: 
- Split tasks logically
- Add or modify based on previous errors
- Output a SINGLE task to do next (one at a time)

User Input:
{query}

History: {history}
"""
    response = llm([HumanMessage(content=prompt)])
    content = response.content.strip()
    return {
        "task": content,
        "input": query,
        "result": state.get("result", ""),
        "history": history
    }

def tool_agent_fn(state: dict) -> dict:
    """
    Executes the task using the best matching tool.
    """
    task = state.get("task")
    if not task:
        return {"result": "No task provided."}

    # try:
    #     result = llm_new.invoke(task)
    #     return {"result": result}

    try:
        result = agent.run(task)
        return {"result": result}
    except Exception as e:
        return {"result": f"ToolAgent Error: {str(e)}"}

class FeedbackAgent:
    def refine_task(self, task, result):
        if "error" in result:
            return task + " (refined)"
        return task
