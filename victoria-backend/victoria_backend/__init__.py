import os
from victoria_backend.lib.spa_static_files import SPAStaticFiles
from victoria_backend.api import api_router
from fastapi import FastAPI
import uvicorn

frontend_path = os.environ.get('FRONTEND_PATH', '../victoria-frontend/build')
index_path = os.path.join(frontend_path, 'index.html')
port = int(os.environ.get('VICTORIA_PORT', 5001))
address = os.environ.get('VICTORIA_ADDRESS', "127.0.0.1")
app = FastAPI()

# Serve the API
app.include_router(api_router, prefix="/api")

# Serve the frontend SPA
app.mount("/", SPAStaticFiles(directory=frontend_path))

def main():
    uvicorn.run("victoria_backend:app", host=address, port=port, reload=True)
