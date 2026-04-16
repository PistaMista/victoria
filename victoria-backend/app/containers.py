from app.config import settings
from app.services.db import DatabaseService
from app.services.auth import AuthService
from app.services.user import UserService
from app.services.monologues import MonologueService
from app.services.monologues.dispatcher import DispatcherService
from app.services.monologues.runner import RunnerService
from app.services.monologues.runner.monologue_thread import AgenticMonologueThread
from app.services.llm import LLMService
from app.services.action import ActionService
from app.services.trigger import TriggerService
from app.services.agent import AgentService
from app.services.chat import ChatService
from app.services.event_bus import EventBusService
from dependency_injector import containers, providers


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            ".interfaces.rest_api.auth",
            ".interfaces.rest_api.action_repos",
            ".interfaces.rest_api.actions",
            ".interfaces.rest_api.agents",
            ".interfaces.rest_api.chats",
            ".interfaces.rest_api.connections",
            ".interfaces.rest_api.events",
            ".interfaces.rest_api.exchanges",
            ".interfaces.rest_api.models",
            ".interfaces.rest_api.monologues",
            ".interfaces.rest_api.queries",
            ".interfaces.rest_api.triggers",
            ".interfaces.rest_api.users",
            ".interfaces.rest_api.webhooks",
            ".interfaces.websocket",
        ]
    )

    config = providers.Configuration(pydantic_settings=[settings])

    event_bus = providers.Singleton(EventBusService)

    db = providers.Singleton(DatabaseService, db_url=config.DATABASE_URL)

    llm = providers.Singleton(LLMService, database_service=db)

    action = providers.Singleton(ActionService, database_service=db)

    monologue = providers.Singleton(
        MonologueService,
        database_service=db,
        action_service=action,
        event_bus_service=event_bus,
    )

    agentic_thread_factory = providers.Factory(
        AgenticMonologueThread,
        monologue_service=monologue,
        llm_service=llm,
        action_service=action,
    )
    runner = providers.Singleton(
        RunnerService,
        db_service=db,
        event_bus_service=event_bus,
        thread_factory=agentic_thread_factory.provider,
        thread_limit=4,
    )
    dispatcher = providers.Singleton(
        DispatcherService,
        db_service=db,
        runner_service=runner,
        event_bus_service=event_bus,
        base_url=providers.Callable(lambda c: f"{c['ADDRESS']}:{c['PORT']}", config),
    )

    trigger = providers.Singleton(TriggerService, database_service=db)

    chat = providers.Singleton(
        ChatService,
        database_service=db,
        trigger_service=trigger,
        event_bus_service=event_bus,
    )

    agent = providers.Singleton(AgentService, database_service=db)

    user = providers.Singleton(UserService, db_service=db)

    auth = providers.Singleton(
        AuthService,
        user_service=user,
        jwt_secret=config.JWT_SECRET,
        login_lifetime=2592000,
    )
