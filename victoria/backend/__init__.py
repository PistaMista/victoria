from langchain_ollama import ChatOllama
from langchain_core.messages import AIMessage
from flask import Flask
from argparse import ArgumentParser
from waitress import serve

app = Flask(__name__)
parser = ArgumentParser(
            prog='Victoria',
            description='An all-purpose AI assistant')
parser.add_argument('-a', '--host-address')
parser.add_argument('-p', '--port')

def main():
    args = parser.parse_args()
    serve(app, host=args.host_address or "127.0.0.1", port=args.port or 5000)

