from fastapi import APIRouter
from .auth import router as auth_router
from .action_repos import router as action_repos_router
from .actions import router as actions_router
from .agents import router as agents_router
from .chats import router as chats_router
from .connections import router as connections_router
from .events import router as events_router
from .exchanges import router as exchanges_router
from .models import router as models_router
from .monologues import router as monologues_router
from .queries import router as queries_router
from .triggers import router as triggers_router
from .users import router as users_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(action_repos_router, prefix="/action-repos", tags=["action-repos"])
api_router.include_router(actions_router, prefix="/actions", tags=["actions"])
api_router.include_router(agents_router, prefix="/agents", tags=["agents"])
api_router.include_router(chats_router, prefix="/chats", tags=["chats"])
api_router.include_router(connections_router, prefix="/connections", tags=["connections"])
api_router.include_router(events_router, prefix="/events", tags=["events"])
api_router.include_router(exchanges_router, prefix="/exchanges", tags=["exchanges"])
api_router.include_router(models_router, prefix="/models", tags=["models"])
api_router.include_router(monologues_router, prefix="/monologues", tags=["monologues"])
api_router.include_router(queries_router, prefix="/queries", tags=["queries"])
api_router.include_router(triggers_router, prefix="/triggers", tags=["triggers"])
api_router.include_router(users_router, prefix="/users", tags=["users"])
