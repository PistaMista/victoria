import os
from app.lib.spa_static_files import SPAStaticFiles
from app.api import api_router
from app.config import settings
from fastapi import FastAPI
from app.db import run_migrations_on_url
import uvicorn

def create_app() -> FastAPI:
    app = FastAPI()

    app.include_router(api_router, prefix="/api")
    if settings.FRONTEND_PATH:
        app.mount("/", SPAStaticFiles(directory=settings.FRONTEND_PATH))
        
    return app

def main():
    app = create_app()
    run_migrations_on_url(settings.DATABASE_URL)
    uvicorn.run(app, host=settings.ADDRESS, port=settings.PORT)
