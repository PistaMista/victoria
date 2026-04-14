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
from app.services.auth import AuthService
from app.services.user import UserService
from app.services.action import ActionService
from app.services.trigger import TriggerService
from app.services.monologues.dispatcher import DispatcherService
from app.services.monologues.runner import RunnerService
from app.services.monologues.runner.monologue_thread import AgenticMonologueThread
from app.services.monologues import MonologueService
from app.services.chat import ChatService
from app.services.agent import AgentService


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

    app.container.db.override(
        providers.Singleton(
            TestDatabaseService, session_factory=sessionmaker(db_connection)
        )
    )
    return app


@pytest.fixture(scope="function")
def user():
    return User(id=1, username="John", role=Role.USER)


@pytest.fixture(scope="function")
def db_mock():
    return mock.MagicMock()


@pytest.fixture(scope="function")
def event_bus_mock():
    return mock.MagicMock()


@pytest.fixture(scope="function")
def user_mock():
    return mock.MagicMock()


@pytest.fixture(scope="function")
def auth_mock():
    return mock.MagicMock()


@pytest.fixture(scope="function")
def monologue_mock():
    return mock.MagicMock()


@pytest.fixture(scope="function")
def dispatcher_mock():
    return mock.MagicMock()


@pytest.fixture(scope="function")
def runner_mock():
    return mock.MagicMock()


@pytest.fixture(scope="function")
def thread_factory_mock():
    return mock.MagicMock()


@pytest.fixture(scope="function")
def chat_mock():
    return mock.MagicMock()


@pytest.fixture(scope="function")
def action_mock():
    return mock.MagicMock()


@pytest.fixture(scope="function")
def trigger_mock():
    return mock.MagicMock()


@pytest.fixture(scope="function")
def agent_mock():
    return mock.MagicMock()


@pytest.fixture(scope="function")
def llm_mock():
    return mock.MagicMock()


@pytest.fixture(scope="function")
def mock_app(
    db_mock,
    event_bus_mock,
    dispatcher_mock,
    user_mock,
    auth_mock,
    monologue_mock,
    runner_mock,
    thread_factory_mock,
    chat_mock,
    action_mock,
    trigger_mock,
    agent_mock,
    llm_mock,
):
    app = create_app()

    app.container.db.override(db_mock)
    app.container.event_bus.override(event_bus_mock)
    app.container.dispatcher.override(dispatcher_mock)
    app.container.user.override(user_mock)
    app.container.auth.override(auth_mock)
    app.container.monologue.override(monologue_mock)
    app.container.runner.override(runner_mock)
    app.container.agentic_thread_factory.override(thread_factory_mock)
    app.container.chat.override(chat_mock)
    app.container.action.override(action_mock)
    app.container.trigger.override(trigger_mock)
    app.container.agent.override(agent_mock)
    app.container.llm.override(llm_mock)

    return app


@pytest.fixture(scope="function")
def client(app):
    return TestClient(app)


@pytest.fixture(scope="function")
def mock_client(mock_app):
    return TestClient(mock_app)


@pytest.fixture(scope="function")
def admin_client(client, db_session):
    user = User(
        username="admin",
        password_hash=b"$2b$12$o8CqurHMoPKWzga2oohzdu0zpukOChhEdEdSBZO1hCZAeRyl5jtJa".decode(
            "utf-8"
        ),
        role=Role.ADMIN,
    )
    user2 = User(
        username="user",
        password_hash=b"$2b$12$o8CqurHMoPKWzga2oohzdu0zpukOChhEdEdSBZO1hCZAeRyl5jtJa".decode(
            "utf-8"
        ),
        role=Role.USER,
    )
    db_session.add(user)
    db_session.add(user2)
    db_session.flush()

    client.post("/api/auth/login", json={"username": "admin", "password": "actual"})

    return client


@pytest.fixture(scope="function")
def user_client(client, db_session):
    user = User(
        username="admin",
        password_hash=b"$2b$12$o8CqurHMoPKWzga2oohzdu0zpukOChhEdEdSBZO1hCZAeRyl5jtJa".decode(
            "utf-8"
        ),
        role=Role.ADMIN,
    )
    user2 = User(
        username="user",
        password_hash=b"$2b$12$o8CqurHMoPKWzga2oohzdu0zpukOChhEdEdSBZO1hCZAeRyl5jtJa".decode(
            "utf-8"
        ),
        role=Role.USER,
    )
    db_session.add(user)
    db_session.add(user2)
    db_session.flush()

    client.post("/api/auth/login", json={"username": "user", "password": "actual"})

    return client
