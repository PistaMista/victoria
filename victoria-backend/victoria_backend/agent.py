from typing import TypedDict, Annotated, Union, Sequence
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.messages import BaseMessage, AIMessage, SystemMessage
from langchain_core.agents import AgentFinish, AgentAction
from langchain.agents import create_react_agent

import operator
import pprint
from victoria_backend.tools import tools

from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

import os

class AgentState(TypedDict):
    """The current state of the agent."""
    messages: Annotated[Sequence[BaseMessage], operator.add]

_llm = ChatOllama(
    model=os.environ.get('VICTORIA_OLLAMA_MODEL', 'llama3.1'),
    base_url=os.environ.get('VICTORIA_OLLAMA_ADDRESS', 'http://localhost:11434'),
    num_ctx=16384
).bind_tools(tools)
_tool_node = ToolNode(tools)

def run_agent(state: AgentState):
    system = SystemMessage(
        content="""
        Your name is Victoria and you are a helpful and empathetic AI assistant.
        
        In the user message are given instructions on how to use tools you are given. Despite the
        instructions, you do not have to use them. Keep your responses on point, USE THE TOOLS ONLY
        IF THEY WOULD HELP WITH THE ACTUAL USER MESSAGE AT THE END OR THE PRIOR CONVERSATION. Otherwise, chat
        like normal, speak about the tools only when asked.
        """
    )

    print("")
    print("Running agent...")
    print("Messages:")
    pprint.pp(state["messages"])

    response = _llm.invoke(
        [system] + state["messages"]
    )
    print("Response:")
    pprint.pp([response])
    return { "messages": [response] }
    
def should_continue(state: AgentState):
    last_message = state["messages"][-1]
    
    if not isinstance(last_message, AIMessage) or not last_message.tool_calls:
        return "end"
    else:
        return "continue"

_graph_builder = StateGraph(AgentState)

_graph_builder.add_node("agent", run_agent)
_graph_builder.add_node("executor", _tool_node)

_graph_builder.set_entry_point('agent')
_graph_builder.add_conditional_edges(
    "agent",
    should_continue,

    {
        "continue": "executor",
        "end": END
    }
)
_graph_builder.add_edge('executor', 'agent')

agent = _graph_builder.compile()


