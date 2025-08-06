import os
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
from app.lib.spa_static_files import SPAStaticFiles
from app.api import api_router
from app.config import settings
from fastapi import FastAPI
from app.db import run_db_migrations
from app.db.session import get_db_session
from app.monologues.dispatcher import Dispatcher
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start the monologue dispatcher when the app starts
    def get_db():
        getter = app.dependency_overrides.get(get_db_session, get_db_session)
        return getter()

    dispatcher = Dispatcher(get_db_func=get_db)
    dispatcher.start()
    yield
    # Stop the monologue dispatcher when the app stops
    dispatcher.stop()

def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    app.include_router(api_router, prefix="/api")
    if settings.FRONTEND_PATH:
        app.mount("/", SPAStaticFiles(directory=settings.FRONTEND_PATH))
    
    return app

def main():
    app = create_app()
    run_db_migrations()
    uvicorn.run(app, host=settings.ADDRESS, port=settings.PORT)
