import os
from alembic.config import Config
from alembic import command
from app.config import settings

def run_db_migrations():
    config = Config()
    parent_dir = os.path.dirname(__file__)
    script_location = os.path.join(parent_dir, "../alembic")
    config.set_main_option('script_location', script_location)
    command.upgrade(config, "head")