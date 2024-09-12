from langchain_ollama import ChatOllama
from langchain_core.messages import AIMessage
from flask import Flask, send_from_directory, request
from argparse import ArgumentParser
from waitress import serve
import os
from time import sleep
from llm import get_next_ai_message

app = Flask(__name__, static_folder=os.environ['FRONTEND_PATH'] or '../../victoria-frontend/build')
parser = ArgumentParser(
            prog='Victoria',
            description='An all-purpose AI assistant')
parser.add_argument('-a', '--host-address')
parser.add_argument('-p', '--port')

@app.route("/")
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route("/<path:path>")
def static_files(path):
    if os.path.isfile(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)   
    elif os.path.isdir(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path + '/index.html')
    else:
        return index()

@app.route("/api/chat", methods=[ "POST" ])
def chat():
    response = get_next_ai_message(request.json["messages"])    
    sleep(5.0)
    
    return response

def main():
    args = parser.parse_args()
    serve(app, host=args.host_address or "127.0.0.1", port=args.port or 5001)

