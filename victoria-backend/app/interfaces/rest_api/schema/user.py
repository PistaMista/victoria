from pydantic import BaseModel
from pydantic.types import StringConstraints
from app.model.user import User, Role
from app.services.user import UserDiff
from typing import Literal, Annotated, List, Optional


class UserListItemResponse(BaseModel):
    id: int
    username: str
    role: Literal['user', 'admin']

class UserResponse(BaseModel):
    id: int
    username: str
    newPassword: Literal[""] = ""
    role: Literal['user', 'admin']
    permittedActions: List[int]
    permittedTriggers: List[int]

def to_user_list_item_response(x: User) -> UserListItemResponse:
    return UserListItemResponse(
        id=x.id,
        username=x.username,
        role='user' if x.role == Role.USER else 'admin'
    )

def to_user_response(x: User) -> UserResponse:
    return UserResponse(
        id=x.id,
        username=x.username,
        role='user' if x.role == Role.USER else 'admin',
        permittedActions=[a.id for a in x.allowed_actions],
        permittedTriggers=[t.id for t in x.allowed_triggers]
    )

class UserLogin(BaseModel):
    username: str
    password: str

Username = Annotated[str, StringConstraints(min_length=3)]
Password = Annotated[str, StringConstraints(min_length=3)]

class UserRegister(BaseModel):
    username: Username
    password: Password

class UserCreate(BaseModel):
    username: str
    newPassword: Password
    role: Literal['user', 'admin']
    permittedActions: List[int]
    permittedTriggers: List[int]

class UserUpdate(BaseModel):
    username: Optional[str] = None
    newPassword: Optional[Password] = None
    role: Optional[Literal['user', 'admin']] = None
    permittedActions: Optional[List[int]] = None
    permittedTriggers: Optional[List[int]] = None

    def to_diff(self) -> UserDiff:
        role = None
        if self.role is not None:
            role = Role.ADMIN if self.role == 'admin' else Role.USER

        return UserDiff(
            username=self.username,
            new_password=self.newPassword,
            role=role,
            permitted_action_ids=self.permittedActions,
            permitted_trigger_ids=self.permittedTriggers
        )


