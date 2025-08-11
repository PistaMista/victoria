import pytest
from typing import Callable
from unittest import mock
from app.main import create_app
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, Connection
from sqlalchemy.orm import Session, sessionmaker
from testcontainers.postgres import PostgresContainer
from dependency_injector import providers
from app.config import settings
from app.model.user import User, Role
from app.services.db import DatabaseService


postgres = PostgresContainer("postgres")

@pytest.fixture(scope="session")
def db_container(request):
    postgres.start()
    
    def remove_container():
        postgres.stop()
    
    request.addfinalizer(remove_container)
    
    db_url = postgres.get_connection_url()
    database_service = DatabaseService(db_url=db_url)
    database_service.run_db_migrations()
    return db_url

@pytest.fixture(scope="session")
def db_engine(db_container):
    engine = create_engine(db_container)
    yield engine
    engine.dispose()


@pytest.fixture(scope="function")
def db_connection(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()
    yield connection
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def db_factory(db_connection):
    return sessionmaker(db_connection)

@pytest.fixture(scope="function")
def db_session(db_connection):
    Session = sessionmaker(db_connection)
    session = Session()
    yield session
    session.close()


class TestDatabaseService(DatabaseService):
    def __init__(self, session_factory: Callable[[], Session]):
        self._session_factory = session_factory

@pytest.fixture(scope="function")
def app(db_connection):
    app = create_app()
    
    # def db_session_override():
    #     session = Session(db_connection)
    #     try:
    #         yield session
    #     finally:
    #         session.close()

    with app.container.db.override(providers.Singleton(
        TestDatabaseService,
        session_factory=sessionmaker(db_connection)
    )):
        yield app

@pytest.fixture(scope="function")
def client(app):
    return TestClient(app)


@pytest.fixture(scope="function")
def admin_client(client, db_session):
    user = User(
        username="admin", 
        password_hash=b'$2b$12$o8CqurHMoPKWzga2oohzdu0zpukOChhEdEdSBZO1hCZAeRyl5jtJa'.decode('utf-8'),
        role=Role.ADMIN
    )
    user2 = User(
        username="user", 
        password_hash=b'$2b$12$o8CqurHMoPKWzga2oohzdu0zpukOChhEdEdSBZO1hCZAeRyl5jtJa'.decode('utf-8'),
        role=Role.USER
    )
    db_session.add(user)
    db_session.add(user2)
    db_session.flush()
    
    client.post('/api/auth/login', json={
        "username": "admin",
        "password": "actual"
    })
    
    return client

@pytest.fixture(scope="function")
def user_client(client, db_session):
    user = User(
        username="admin", 
        password_hash=b'$2b$12$o8CqurHMoPKWzga2oohzdu0zpukOChhEdEdSBZO1hCZAeRyl5jtJa'.decode('utf-8'),
        role=Role.ADMIN
    )
    user2 = User(
        username="user", 
        password_hash=b'$2b$12$o8CqurHMoPKWzga2oohzdu0zpukOChhEdEdSBZO1hCZAeRyl5jtJa'.decode('utf-8'),
        role=Role.USER
    )
    db_session.add(user)
    db_session.add(user2)
    db_session.flush()
    
    client.post('/api/auth/login', json={
        "username": "user",
        "password": "actual"
    })
    
    return client