from langchain_ollama import ChatOllama
from langchain_core.messages import AIMessage, HumanMessage
from langchain.agents import AgentExecutor, create_tool_calling_agent, tool
from langchain_core.prompts import ChatPromptTemplate
from datetime import datetime
import os

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", """
        Your name is Victoria and you are a helpful and empathetic AI assistant.
        Do not mention that you're calling tools and only call them when you need to.
        """),
        ("placeholder", "{conversation}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)
llm = ChatOllama(
    model=os.environ.get('VICTORIA_OLLAMA_MODEL', 'default'),
    base_url=os.environ.get('VICTORIA_OLLAMA_ADDRESS', 'http://localhost:11434')
)

@tool
def today():
    """Returns the current date in YYYY-MM-DD DAY_OF_WEEK format."""
    return datetime.today().strftime('%Y-%m-%d %A')
    

@tool
def show_tasks() -> [str]:
    """Returns a list of currently planned tasks (aka. the calendar)."""
    
    return [
        "Monday: Mow the lawn"
    ]

@tool
def add(a: int, b: int) -> int:
    """Adds a and b."""
    return a + b

@tool
def multiply(a: int, b: int) -> int:
    """Multiplies a and b."""
    return a * b

tools = [today, show_tasks, add, multiply]
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