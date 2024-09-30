from typing import TypedDict, Annotated, List, Union
from langchain_core.messages import BaseMessage, AIMessage
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_ollama import ChatOllama
import operator
from victoria_backend.tools import tools

from langgraph.graph import StateGraph

import os

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], operator.add]
    # agent_outcome: AgentFinish | AgentAction | None
    # intermediate_steps: Annotated[list[tuple[AgentAction, str]], operator.add]

_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", """
        Your name is Victoria and you are a helpful and empathetic AI assistant. Ask
        helpful questions to help figure out the root cause of the issue at hand.
        """),
        ("placeholder", "{messages}"),
    ]
)

_llm = ChatOllama(
    model=os.environ.get('VICTORIA_OLLAMA_MODEL', 'default'),
    base_url=os.environ.get('VICTORIA_OLLAMA_ADDRESS', 'http://localhost:11434'),
    num_ctx=16384
)
_llm_with_prompt = _prompt | _llm


def chatbot(state: AgentState):
    return {
        "messages": [
            _llm_with_prompt.invoke(
                {'messages': state["messages"]}
            )
        ]
    }

_graph_builder = StateGraph(AgentState)
_graph_builder.add_node("chatbot", chatbot)
_graph_builder.set_entry_point("chatbot")
_graph_builder.set_finish_point("chatbot")

agent = _graph_builder.compile()


