from app.config import settings
from app.services.db import DatabaseService
from app.services.auth import AuthService
from app.services.user import UserService
from app.services.monologues.dispatcher import DispatcherService
from dependency_injector import containers, providers

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            ".interfaces.rest_api.auth"
        ]
    )
    
    config = providers.Configuration(
        pydantic_settings=[settings]
    )
    
    db = providers.Singleton(
        DatabaseService,
        db_url=config.DATABASE_URL
    )
    dispatcher = providers.Singleton(
        DispatcherService,
        db_service=db
    )
    user = providers.Factory(
        UserService,
        db_service=db
    )
    auth = providers.Factory(
        AuthService,
        user_service=user,
        jwt_secret=config.JWT_SECRET,
        login_lifetime=2592000
    )