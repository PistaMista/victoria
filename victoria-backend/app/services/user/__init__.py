from app.services.db import DatabaseService
from bcrypt import hashpw, gensalt
from typing import Optional, List
from app.model.user import User, Role
from app.model.agent import Agent
from app.model.monologue import Monologue, MonologueStatus
from app.model.action import Action
from app.model.trigger import Trigger
from sqlalchemy import select
from pydantic import BaseModel

class UserService:
    def __init__(self, db_service: DatabaseService):
        self._db = db_service

    def get_all_users(self) -> List[User]:
        """Gets all registered Users."""
        with self._db.session() as db:
            res = db.scalars(
                select(User)
            ).all()

            return res
    
    def get_user_by_running_monologue_agent_token(self, token: bytes) -> User:
        """Gets the owner of the Monologue given by the token, if it is running."""
        with self._db.session() as db:
            res = db.scalar(
                select(User)
                .join(User.agents)
                .join(Agent.monologues)
                .where(
                    Monologue.agent_token == token,
                    Monologue.status == MonologueStatus.RUNNING
                )
            )

            if res is None:
                raise NonexistentUserError("")

            return res

    def update_user(self, id: int, changes: "UserDiff"):
        """Updates the given User."""
        pass
        
    def create_user(self, username: str, password: str, role: Role, permitted_action_ids: List[int] = [], permitted_trigger_ids: List[int] = []) -> int:
        with self._db.session() as db:
            existing_user = db.scalars(
                    select(User).where(User.username == username)
                ).first()
            
            if existing_user is not None:
                raise UserExistsError(username)

            new_user = User(
                username=username,
                password_hash=hashpw(password.encode('utf-8'), gensalt()).decode('utf-8'),
                role=role
            )

            permitted_actions = db.scalars(
                select(Action).where(Action.id.in_(permitted_action_ids))
            ).all()
            permitted_triggers = db.scalars(
                select(Trigger).where(Trigger.id.in_(permitted_trigger_ids))
            ).all()

            if len(permitted_actions) < len(permitted_action_ids):
                raise InvalidUserSettingError("Invalid action ID for permitted action")
            
            if len(permitted_triggers) < len(permitted_trigger_ids):
                raise InvalidUserSettingError("Invalid trigger ID from permitted trigger")

            new_user.allowed_actions = permitted_actions
            new_user.allowed_triggers = permitted_triggers

            db.add(new_user)
            db.commit()

            return new_user.id
    
    def is_any_user_registered(self) -> bool:
        with self._db.session() as db:
            first_user = db.scalars(
                select(User)
            ).first()

            return first_user is not None

    def get_user_by_id(self, id: int) -> User:
        # TODO: Throw NonexistentUserError when the user does not exist
        with self._db.session() as db:
            user = db.scalar(
                select(User).where(User.id == id)
            )

            return user
    
    def get_user_by_name(self, username: str) -> Optional[User]:
        with self._db.session() as db:
            user = db.scalar(
                select(User).where(User.username == username)
            )
            
            return user
    
    def delete_user_by_id(self, id: int):
        with self._db.session() as db:
            user = db.scalar(
                select(User).where(User.id == id)
            )
            
            if user:
                db.delete(user)
                db.commit()

class UserDiff(BaseModel):
    username: Optional[str] = None
    new_password: Optional[str] = None
    role: Optional[Role] = None
    permitted_action_ids: Optional[List[int]] = None
    permitted_trigger_ids: Optional[List[int]] = None

class InvalidUserSettingError(Exception):
    def __init__(self, msg: str):
        super().__init__(f"tried to set an invalid value for property of user: {msg}")

class NonexistentUserError(Exception):
    def __init__(self, id_or_name: int | str):
        super().__init__(f"nonexistent user {id_or_name}")

class UserExistsError(Exception):
    def __init__(self, username: str):
        super().__init__(f"user {username} already exists")
