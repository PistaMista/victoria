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
            ".interfaces.rest_api.queries"
        ]
    )
    
    config = providers.Configuration(
        pydantic_settings=[settings]
    )
    
    db = providers.Singleton(
        DatabaseService,
        db_url=config.DATABASE_URL
    )

    llm = providers.Singleton(
        LLMService,
        database_service=db
    )

    action = providers.Singleton(
        ActionService,
        database_service=db
    )

    monologue = providers.Singleton(
        MonologueService,
        database_service=db,
        action_service=action
    )

    agentic_thread_factory = providers.Factory(
        AgenticMonologueThread,
        monologue_service=monologue,
        llm_service=llm,
        action_service=action
    )
    runner = providers.Singleton(
        RunnerService,
        db_service=db,
        thread_factory=agentic_thread_factory,
        thread_limit=4
    )
    dispatcher = providers.Singleton(
        DispatcherService,
        db_service=db,
        runner_service=runner
    )

    chat = providers.Singleton(
        ChatService
    )

    trigger = providers.Singleton(
        TriggerService
    )

    agent = providers.Singleton(
        AgentService
    )

    user = providers.Singleton(
        UserService,
        db_service=db
    )

    auth = providers.Singleton(
        AuthService,
        user_service=user,
        jwt_secret=config.JWT_SECRET,
        login_lifetime=2592000
    )
