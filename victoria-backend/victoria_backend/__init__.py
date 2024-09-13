from flask import Flask, send_from_directory, request
from waitress import serve
import os
from time import sleep
from victoria_backend.llm import get_next_ai_message

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

def main():
    serve(app, host=os.environ.get('VICTORIA_ADDRESS', "127.0.0.1"), port=os.environ.get('VICTORIA_PORT', 5001))

