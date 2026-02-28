import os
from contextlib import contextmanager, AbstractContextManager
from typing import Callable
from alembic.config import Config
from alembic import command
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


class DatabaseService:
    def __init__(self, db_url: str):
        # args = { "check_same_thread": False }
        args = {}
        self._db_url = db_url
        self._engine = create_engine(db_url, connect_args=args)
        self._session_factory = sessionmaker(self._engine)

    def get_session_factory(self) -> Callable[[], Session]:
        return self._session_factory

    @contextmanager
    def session(self) -> Callable[..., AbstractContextManager[Session]]:
        session: Session = self.get_session_factory()()

        try:
            yield session
        finally:
            session.close()

    def run_db_migrations(self):
        config = Config()
        parent_dir = os.path.dirname(__file__)
        script_location = os.path.join(parent_dir, "../../alembic")
        config.set_main_option("script_location", script_location)
        config.set_main_option("sqlalchemy.url", self._db_url)
        command.upgrade(config, "head")
