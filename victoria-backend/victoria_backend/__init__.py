import os
from victoria_backend.lib.spa_static_files import SPAStaticFiles
from victoria_backend.api import api_router
from fastapi import FastAPI
from alembic import command
from alembic.config import Config
import uvicorn

frontend_path = os.environ.get('VICTORIA_FRONTEND_PATH')
port = int(os.environ.get('VICTORIA_PORT', 5001))
address = os.environ.get('VICTORIA_ADDRESS')
database_url = os.environ.get('VICTORIA_DATABASE_URL')

app = FastAPI()

# Serve the API
app.include_router(api_router, prefix="/api")

# Serve the frontend SPA
app.mount("/", SPAStaticFiles(directory=frontend_path))

def migrate_db():
    config = Config()
    parent_dir = os.path.dirname(__file__)
    script_location = os.path.join(parent_dir, "../alembic")
    config.set_main_option('script_location', script_location)
    command.upgrade(config, "head")

def main():
    migrate_db()
    uvicorn.run("victoria_backend:app", host=address, port=port, reload=True)
