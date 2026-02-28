from fastapi import status, APIRouter, Depends, HTTPException
from app.model.chat import Chat
from app.model.user import User
from app.services.action import ActionService, NonexistentActionRepositoryError
from typing import Annotated, List
from dependency_injector.wiring import inject, Provide
from .dependencies.auth import get_admin_user
from .schema.action_repos import (
    ActionRepository,
    ActionRepositoryCreate,
    ActionRepositoryUpdate,
)
from app.containers import Container

router = APIRouter()


@router.get("/", response_model=List[ActionRepository])
@inject
async def list_repos(
    _: Annotated[User, Depends(get_admin_user)],
    action_service: Annotated[ActionService, Depends(Provide[Container.action])],
) -> List[ActionRepository]:
    repos = action_service.get_all_action_repositories()
    return [ActionRepository.model_validate(repo) for repo in repos]


@router.get("/{id}", response_model=ActionRepository)
@inject
async def get_repo(
    id: int,
    _: Annotated[User, Depends(get_admin_user)],
    action_service: Annotated[ActionService, Depends(Provide[Container.action])],
) -> ActionRepository:
    try:
        repo = action_service.get_action_repository_by_id(id)
        return ActionRepository.model_validate(repo)
    except NonexistentActionRepositoryError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))


@router.post("/")
@inject
async def create_repo(
    body: ActionRepositoryCreate,
    _: Annotated[User, Depends(get_admin_user)],
    action_service: Annotated[ActionService, Depends(Provide[Container.action])],
) -> None:
    action_service.add_action_repository(name=body.name, url=body.url)


@router.put("/{id}")
@inject
async def update_repo(
    id: int,
    body: ActionRepositoryUpdate,
    _: Annotated[User, Depends(get_admin_user)],
    action_service: Annotated[ActionService, Depends(Provide[Container.action])],
) -> bool:
    try:
        action_service.update_action_repository(id, body.to_diff())
        return True
    except NonexistentActionRepositoryError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))


@router.delete("/{id}")
@inject
async def delete_repo(
    id: int,
    _: Annotated[User, Depends(get_admin_user)],
    action_service: Annotated[ActionService, Depends(Provide[Container.action])],
):
    try:
        action_service.remove_action_repository(id)
        return True
    except NonexistentActionRepositoryError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
