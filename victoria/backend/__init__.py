from langchain_ollama import ChatOllama
from langchain_core.messages import AIMessage
from flask import Flask
from argparse import ArgumentParser

app = Flask(__name__)
parser = ArgumentParser(
            prog='Victoria',
            description='An all-purpose AI assistant')
parser.add_argument('-a', '--host-address')
parser.add_argument('-p', '--port')


@app.route("/")
def hello_world():
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

    return ai_msg.content

def main():
    args = parser.parse_args()
    app.run(host=args.host_address, port=args.port)

    
