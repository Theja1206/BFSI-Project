#agent_graph.py
import os
from langchain_anthropic import ChatAnthropic
from typing import Annotated, Sequence
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage, HumanMessage, ToolMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from mcp_server import get_customer_financial_ratios, check_credit_bureau_flags

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

tools = [get_customer_financial_ratios, check_credit_bureau_flags]

api_key = os.environ.get("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("ANTHROPIC_API_KEY environment variable is missing")

model = ChatAnthropic(
    model="claude-opus-4-8"
).bind_tools(tools)

def call_card_analyst(state: AgentState):
    messages = state['messages']
    response = model.invoke(messages)
    return {"messages": [response]}

def execute_mcp_tools(state: AgentState):
    messages = state['messages']
    last_message = messages[-1]#reading from last.
    tool_outputs = []

    for tool_call in last_message.tool_calls:
        tool_name = tool_call['name']
        args = tool_call['args']

        if tool_name == "get_customer_financial_ratios":
            res = get_customer_financial_ratios(**args)
        elif tool_name == "check_credit_bureau_flags":
            res = check_credit_bureau_flags(**args)
        else:
            res = "Tool Error Tool '{tool_name}' not recognized"

        tool_outputs.append(ToolMessage(content=str(res), tool_call_id=tool_call['id']))
    return {'messages': tool_outputs}

def route_next_step(state:AgentState):
    last_message = state['messages'][-1]
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        return "call_tools"
    return END

workflow = StateGraph(AgentState)

workflow.add_node("analyst", call_card_analyst)
workflow.add_node("call_tools", execute_mcp_tools)

workflow.add_edge(START, "analyst")
workflow.add_conditional_edges("analyst", route_next_step)
workflow.add_edge("call_tools", "analyst")

credit_agent_app = workflow.compile()




