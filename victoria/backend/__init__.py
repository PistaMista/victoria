from langchain_ollama import ChatOllama
from langchain_core.messages import AIMessage


def main():
    llm = ChatOllama(
            model = "dolphin-llama3"
        )

    messages = [
                (
                    "system",
                    "You are a helpful assistant that translates English to French. Translate the user sentence.",
                ),
                ("human", "I love programming"),
            ]

    ai_msg = llm.invoke(messages)
    print(ai_msg)


