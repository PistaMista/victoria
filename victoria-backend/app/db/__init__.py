import os
from alembic.config import Config
from alembic import command
from app.config import settings

def run_migrations_on_url(url: str):
    config = Config()
    parent_dir = os.path.dirname(__file__)
    script_location = os.path.join(parent_dir, "../../alembic")
    config.set_main_option('sqlalchemy.url', url)
    config.set_main_option('script_location', script_location)
    command.upgrade(config, "head")