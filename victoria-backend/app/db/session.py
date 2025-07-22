from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings

if settings.DATABASE_URL:
    engine = create_engine(settings.DATABASE_URL)
    Session = sessionmaker(engine)

def get_db_session():
    session = Session()
    try:
        yield session
    finally:
        session.close()