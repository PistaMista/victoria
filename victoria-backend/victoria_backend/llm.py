from langchain_ollama import ChatOllama
from langchain_core.messages import AIMessage

def get_next_ai_message(messages):
    print(messages)
    return {
        'type': "assistant",
        'content': "Lol"
    }