from langchain_ollama import ChatOllama
from langchain_core.messages import AIMessage, HumanMessage
import os

chat = ChatOllama(
    model=os.environ.get('VICTORIA_OLLAMA_MODEL', 'default'),
    base_url=os.environ.get('VICTORIA_OLLAMA_ADDRESS', 'http://localhost:11434')
)

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
    response = chat.invoke(messages)
    return from_message_object(response)