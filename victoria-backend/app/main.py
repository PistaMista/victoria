import os
from app.lib.spa_static_files import SPAStaticFiles
from app.api import api_router
from app.config import Settings
from fastapi import FastAPI
from app.db import run_migrations_on_url
import uvicorn

def create_app() -> FastAPI:
    app = FastAPI()

    app.include_router(api_router, prefix="/api")
    if Settings.frontend_path:
        app.mount("/", SPAStaticFiles(directory=Settings.frontend_path))
        
    return app

def main():
    app = create_app()
    run_migrations_on_url(Settings.database_url)
    uvicorn.run(app, host=address, port=port)
