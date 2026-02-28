from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.config import settings
from typing import Generator

if settings.DATABASE_URL:
    args = {"check_same_thread": False}
    engine = create_engine(settings.DATABASE_URL, connect_args=args)
    Session = sessionmaker(engine)


def get_db_session() -> Generator[Session, None, None]:
    session = Session()
    try:
        yield session
    finally:
        session.close()
