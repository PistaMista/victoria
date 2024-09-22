from typing import TypedDict, Annotated, List, Union
from langchain_core.messages import BaseMessage
from langchain_ollama import ChatOllama
import operator
from victoria_backend.tools import tools

from langgraph.graph import StateGraph

import os

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], operator.add]
    # agent_outcome: AgentFinish | AgentAction | None
    # intermediate_steps: Annotated[list[tuple[AgentAction, str]], operator.add]

# _prompt = ChatPromptTemplate.from_messages(
#     [
#         ("system", """
#         Your name is Victoria and you are a helpful and empathetic AI assistant. Ask
#         helpful questions to help figure out the root cause of the issue at hand.

#         Obey the following rules:
#         - You MUST only search the web for casual topics, UNLESS given explicit permission
#         - When including web articles in your response, you MUST include hyperlinks to the articles in the response
#         - When responding with a web search, include the most important hyperlinks to the sources in the response
#         - You do not have to use tool calls all the time
#         - You MUST think step by step
#         """),
#         ("placeholder", "{chat_history}"),
#         ("human", "{input}"),
#         ("placeholder", "{agent_scratchpad}"),
#     ]
# )
_llm = ChatOllama(
    model=os.environ.get('VICTORIA_OLLAMA_MODEL', 'default'),
    base_url=os.environ.get('VICTORIA_OLLAMA_ADDRESS', 'http://localhost:11434'),
    num_ctx=16384
)
#_tool_agent_runnable = create_tool_calling_agent(_llm, tools, _prompt)


def chatbot(state: AgentState):
    return {
        "messages": [_llm.invoke(state["messages"])]
    }

_graph_builder = StateGraph(AgentState)
_graph_builder.add_node("chatbot", chatbot)
_graph_builder.set_entry_point("chatbot")
_graph_builder.set_finish_point("chatbot")

agent = _graph_builder.compile()


