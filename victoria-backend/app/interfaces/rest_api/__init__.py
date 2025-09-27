from fastapi import APIRouter
from .auth import router as auth_router
from .action_repos import router as action_repos_router
from .actions import router as actions_router
from .agents import router as agents_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(action_repos_router, prefix="/action-repos", tags=["action-repos"])
api_router.include_router(actions_router, prefix="/actions", tags=["actions"])
api_router.include_router(agents_router, prefix="/agents", tags=["agents"])
