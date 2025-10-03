from fastapi import APIRouter, status, HTTPException, Depends
from dependency_injector.wiring import inject, Provide
from app.services.user import UserService, UserExistsError, NonexistentUserError, InvalidUserSettingError
from app.model.user import User, Role
from app.containers import Container
from .dependencies.auth import get_admin_user
from .schema.user import UserListItemResponse, to_user_list_item_response, UserCreate, UserResponse, to_user_response, UserUpdate
from typing import Annotated, List


router = APIRouter()

@router.get("/", response_model=List[UserListItemResponse])
@inject
async def list_users(
    _: Annotated[User, Depends(get_admin_user)],
    user_service: Annotated[UserService, Depends(Provide[Container.user])]
) -> List[UserListItemResponse]:
    users = user_service.get_all_users()
    return [to_user_list_item_response(x) for x in users]

@router.post("/", response_model=UserListItemResponse)
@inject
async def create_user(
    body: UserCreate,
    _: Annotated[User, Depends(get_admin_user)],
    user_service: Annotated[UserService, Depends(Provide[Container.user])]
) -> UserListItemResponse:
    try:
        created_id = user_service.create_user(
            username=body.username,
            password=body.newPassword,
            role=Role.ADMIN if body.role == 'admin' else Role.USER,
            permitted_action_ids=body.permittedActions,
            permitted_trigger_ids=body.permittedTriggers
        )
        created_user = user_service.get_user_by_id(id=created_id)
        return to_user_list_item_response(created_user)
    except (UserExistsError, InvalidUserSettingError) as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err)
        )

@router.get("/{id}", response_model=UserResponse)
@inject
async def get_user(
    id: int,
    _: Annotated[User, Depends(get_admin_user)],
    user_service: Annotated[UserService, Depends(Provide[Container.user])]
) -> UserResponse:
    try:
        user = user_service.get_user_by_id(id=id)
        return to_user_response(user)
    except NonexistentUserError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err)
        )

@router.put("/{id}")
@inject
async def update_user(
    id: int,
    body: UserUpdate,
    _: Annotated[User, Depends(get_admin_user)],
    user_service: Annotated[UserService, Depends(Provide[Container.user])]
):
    try:
        user_service.update_user(
            id=id,
            changes=body.to_diff()
        )
    except (UserExistsError, InvalidUserSettingError) as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err)
        )
    except NonexistentUserError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err)
        )

@router.delete("/{id}")
@inject
async def delete_user(
    id: int,
    _: Annotated[User, Depends(get_admin_user)],
    user_service: Annotated[UserService, Depends(Provide[Container.user])]
):
    try:
        user_service.delete_user_by_id(id=id)
    except NonexistentUserError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err)
        )


    
