
import os
from dotenv import load_dotenv
load_dotenv()
GROK_API_KEY = os.getenv("GROK_API_KEY")

from langchain_groq import ChatGroq
llm = ChatGroq(api_key=GROK_API_KEY, model_name="Gemma2-9b-It")
from langchain_core.messages import HumanMessage
from tools import transfer_to_tools_Agent, transfer_to_plan_Agent
from tools import calculator_tool, webscraper_tool, mock_tool, search
from agents import plan_agent_fn, tool_agent_fn

llm_new = llm.bind_tools([transfer_to_tools_Agent, transfer_to_plan_Agent, calculator_tool, webscraper_tool, mock_tool, search])

from langgraph.graph import StateGraph, END
from typing import TypedDict

class AgentState(TypedDict):
    input: str
    task: str
    result: str
    history: list

def decide_to_generate(state):
    result = state.get("result", "").lower()
    if "error" in result:
        return "plan"
    else:
        return "tools"

def llm_checker_fn(state):
    tool_output = state.get("result", "")
    print("🔍 Received tool result:", tool_output)

    if not tool_output:
        return {"result": "⚠️ No tool output found."}

    llm_response = llm.invoke(f"Review this tool output and rewrite it like an article: {tool_output}")
    return {
        "result": llm_response.content
    }

workflow = StateGraph(AgentState)

workflow.add_node("PlanAgent", plan_agent_fn)
workflow.add_node("ToolAgent", tool_agent_fn)

workflow.set_entry_point("PlanAgent")
workflow.add_edge("PlanAgent", "ToolAgent")
workflow.add_conditional_edges(
    "PlanAgent",
    decide_to_generate,
    {
        "plan": "PlanAgent",
        "tools": "ToolAgent",
    },
)
workflow.add_edge("ToolAgent", END)

graph = workflow.compile()

import pprint
input_state = {
    "input": "who is virat kohli?",
    "task": "",
    "result": "",
    "history": []
}

for output in graph.stream(input_state):
    for key, value in output.items():
        pprint.pprint(f"Output from node '{key}':")
        pprint.pprint("---")
        pprint.pprint(value, indent=2, width=80, depth=None)
    pprint.pprint("\n---\n")
