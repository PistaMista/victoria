from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings

if settings.DATABASE_URL:
    args = { "check_same_thread": False }
    engine = create_engine(settings.DATABASE_URL, connect_args=args)
    Session = sessionmaker(engine)

def get_db_session():
    session = Session()
    try:
        yield session
    finally:
        session.close()