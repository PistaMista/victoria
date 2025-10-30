import os
from contextlib import asynccontextmanager
from app.lib.spa_static_files import SPAStaticFiles
from app.interfaces.rest_api import api_router
from app.config import settings
from fastapi import FastAPI
from app.containers import Container
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start the monologue dispatcher when the app starts
    dispatcher = app.container.dispatcher()
    dispatcher.start()
    yield
    # Stop the monologue dispatcher when the app stops
    dispatcher.stop()

def create_app() -> FastAPI:
    container = Container()
    app = FastAPI(lifespan=lifespan)
    app.container = container
    app.mount("/api", api_router)

    if settings.FRONTEND_PATH:
        app.mount("/", SPAStaticFiles(directory=settings.FRONTEND_PATH))
    
    return app

def main():
    app = create_app()

    db = app.container.db()
    db.run_db_migrations()

    app.container.action()
    app.container.trigger()
    app.container.llm()

    uvicorn.run(app, host=settings.ADDRESS, port=settings.PORT)
