from fastapi import status, APIRouter, Depends
from .schema.actions import ActionResponse
from .dependencies.auth import get_non_admin_user, get_admin_user
from app.model.user import User
from app.services.action import ActionService
from dependency_injector.wiring import inject, Provide
from typing import List, Annotated
from app.containers import Container

router = APIRouter()

@router.get("/", response_model=List[ActionResponse])
@inject
def get_permitted_actions(
    user: Annotated[User, Depends(get_non_admin_user)],
    action_service: Annotated[ActionService, Depends(Provide[Container.action])]
):
    actions = action_service.get_user_permitted_actions(user.id)
    return [ActionResponse.model_validate(x) for x in actions]

@router.get("/all", response_model=List[ActionResponse])
@inject
def get_all_actions(
    _: Annotated[User, Depends(get_admin_user)],
    action_service: Annotated[ActionService, Depends(Provide[Container.action])]
):
    actions = action_service.get_all_actions()
    return [ActionResponse.model_validate(x) for x in actions]

