from flask import Flask, send_from_directory, request
from langchain_core.messages import AIMessage, HumanMessage
from waitress import serve
import os
from time import sleep

from victoria_backend.agent import agent

app = Flask(__name__, static_folder=os.environ.get('FRONTEND_PATH', '../../victoria-frontend/build'))

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
    return response

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
    
    new_messages = agent.invoke({
            "messages": messages,
            "agent_outcome": None,
            "intermediate_steps": []
        })["messages"]
    response = new_messages[-1]
    return from_message_object(response)

def main():
    serve(app, host=os.environ.get('VICTORIA_ADDRESS', "127.0.0.1"), port=os.environ.get('VICTORIA_PORT', 5001))

