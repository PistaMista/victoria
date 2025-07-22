import os
from app.lib.spa_static_files import SPAStaticFiles
from app.api import api_router
from fastapi import FastAPI
from alembic import command
from alembic.config import Config
import uvicorn

class App(FastAPI):
    def __init__(self, database_url: str, frontend_path: str | None, **kwargs):
        super().__init__(**kwargs)

        self.database_url: str = database_url
        self.frontend_path: str | None = frontend_path
        
        self.migrate_db()
        
        self.mount_api()
        if self.frontend_path:
            self.mount_spa()

    def migrate_db(self):
        config = Config()
        parent_dir = os.path.dirname(__file__)
        script_location = os.path.join(parent_dir, "../alembic")
        config.set_main_option('sqlalchemy.url', self.database_url)
        config.set_main_option('script_location', script_location)
        command.upgrade(config, "head")
    
    def mount_api(self):
        self.include_router(api_router, prefix="/api")
    
    def mount_spa(self):
        self.mount("/", SPAStaticFiles(directory=self.frontend_path))

def main():
    database_url = os.environ.get('VICTORIA_DATABASE_URL')
    frontend_path = os.environ.get('VICTORIA_FRONTEND_PATH')
    port = int(os.environ.get('VICTORIA_PORT', 5001))
    address = os.environ.get('VICTORIA_ADDRESS')
    
    app = App(database_url=database_url, frontend_path=frontend_path)
    uvicorn.run(app, host=address, port=port)
