from fastapi import status, HTTPException, Depends, APIRouter
from app.services.monologues import MonologueService, NonexistentMonologueError
from dependency_injector.wiring import inject, Provide
from app.model.user import User
from app.containers import Container
from .dependencies.auth import get_non_admin_user
from .schema.monologues import (
    MonologueEnd,
    MonologueListItemResponse,
    MonologueResponse,
    ThoughtResponse,
    to_monologue_list_item_response,
    to_monologue_response,
    to_thought_response,
)
from typing import List, Annotated

router = APIRouter()


@router.get("/", response_model=List[MonologueListItemResponse])
@inject
async def list_monologues(
    user: Annotated[User, Depends(get_non_admin_user)],
    monologue_service: Annotated[
        MonologueService, Depends(Provide[Container.monologue])
    ],
) -> List[MonologueListItemResponse]:
    monologues = monologue_service.get_user_monologues(user_id=user.id)
    return [to_monologue_list_item_response(x) for x in monologues]


@router.get("/{id}", response_model=MonologueResponse)
@inject
async def get_monologue(
    id: int,
    user: Annotated[User, Depends(get_non_admin_user)],
    monologue_service: Annotated[
        MonologueService, Depends(Provide[Container.monologue])
    ],
) -> MonologueResponse:
    try:
        monologue = monologue_service.get_user_monologue(
            user_id=user.id, monologue_id=id
        )
        return to_monologue_response(monologue)
    except NonexistentMonologueError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))


@router.post("/{id}/abort")
@inject
async def abort_monologue(
    id: int,
    user: Annotated[User, Depends(get_non_admin_user)],
    monologue_service: Annotated[
        MonologueService, Depends(Provide[Container.monologue])
    ],
):
    try:
        monologue_service.end_user_monologue(
            user_id=user.id, monologue_id=id, successful=False
        )
    except NonexistentMonologueError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))


@router.post("/{id}/end")
@inject
async def end_monologue(
    id: int,
    body: MonologueEnd,
    user: Annotated[User, Depends(get_non_admin_user)],
    monologue_service: Annotated[
        MonologueService, Depends(Provide[Container.monologue])
    ],
):
    try:
        monologue_service.end_user_monologue(
            user_id=user.id, monologue_id=id, successful=body.successful
        )
    except NonexistentMonologueError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))


@router.get("/{id}/thoughts", response_model=List[ThoughtResponse])
@inject
async def get_monologue_thoughts(
    id: int,
    user: Annotated[User, Depends(get_non_admin_user)],
    monologue_service: Annotated[
        MonologueService, Depends(Provide[Container.monologue])
    ],
) -> List[ThoughtResponse]:
    try:
        thoughts = monologue_service.get_user_monologue_thoughts(
            user_id=user.id, monologue_id=id
        )
        return [to_thought_response(x) for x in thoughts]
    except NonexistentMonologueError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
