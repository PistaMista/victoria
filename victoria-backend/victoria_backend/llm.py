from langchain_ollama import ChatOllama
from langchain_core.messages import AIMessage, HumanMessage
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from datetime import datetime
from victoria_backend.tools import tools
import os

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", """
        Your name is Victoria and you are a helpful and empathetic AI assistant. Ask
        helpful questions to help figure out the root cause of the issue at hand.

        Obey the following rules:
        - You MUST only search the web for casual topics, UNLESS given explicit permission
        - When including web articles in your response, you MUST include hyperlinks to the articles in the response
        - When responding with a web search, include the most important hyperlinks to the sources in the response
        - You do not have to use tool calls all the time
        - You MUST think step by step
        """),
        ("placeholder", "{conversation}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)
llm = ChatOllama(
    model=os.environ.get('VICTORIA_OLLAMA_MODEL', 'default'),
    base_url=os.environ.get('VICTORIA_OLLAMA_ADDRESS', 'http://localhost:11434'),
    num_ctx=16384
)

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

def to_message_object(msg):
    match (msg["type"]):
        case "user":
            return HumanMessage(msg["content"])
        case "assistant":
            return AIMessage(msg["content"])

def from_message_object(msg):
    if type(msg) is HumanMessage:
        return {
            'type': "user",
            'content': msg.content
        }
    elif type(msg) is AIMessage:
        return {
            'type': "assistant",
            'content': msg.content
        }

def get_next_ai_message(messages):
    messages = list(map(to_message_object, messages))
    response = AIMessage(agent_executor.invoke({
        "conversation": messages
    })["output"])
    print(response)
    return from_message_object(response)