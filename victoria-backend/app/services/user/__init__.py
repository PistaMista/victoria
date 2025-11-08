from app.services.db import DatabaseService
from bcrypt import hashpw, gensalt
from typing import Optional, List
from app.model.user import User, Role
from app.model.agent import Agent
from app.model.monologue import Monologue, MonologueStatus
from app.model.action import Action
from app.model.trigger import Trigger
from sqlalchemy import select
from sqlalchemy.orm import joinedload
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
        with self._db.session() as db:
            user = db.scalar(
                select(User).where(User.id == id)
            )

            if user is None:
                raise NonexistentUserError(id)

            if changes.username is not None:
                user.username = changes.username

            if changes.new_password is not None:
                user.password_hash = self._hash_password(changes.new_password)

            if changes.role is not None:
                user.role = changes.role


            if changes.permitted_trigger_ids is not None:
                permitted_triggers = db.scalars(
                    select(Trigger).where(Trigger.id.in_(changes.permitted_trigger_ids))
                ).all()

                if len(permitted_triggers) < len(changes.permitted_trigger_ids):
                    raise InvalidUserSettingError("Invalid trigger ID from permitted trigger")

                user.allowed_triggers = permitted_triggers

                # Disallow newly forbidden triggers for all agents
                for agent in user.agents:
                    agent.allowed_triggers = [t for t in agent.allowed_triggers if t in user.allowed_triggers]

            if changes.permitted_action_ids is not None:
                permitted_actions = db.scalars(
                    select(Action).where(Action.id.in_(changes.permitted_action_ids))
                ).all()

                if len(permitted_actions) < len(changes.permitted_action_ids):
                    raise InvalidUserSettingError("Invalid action ID for permitted action")

                user.allowed_actions = permitted_actions

                # Disallow newly forbidden actions for all agents
                for agent in user.agents:
                    agent.allowed_actions = [t for t in agent.allowed_actions if t in user.allowed_actions]

            db.commit()
        
    def create_user(self, username: str, password: str, role: Role, permitted_action_ids: List[int] = [], permitted_trigger_ids: List[int] = []) -> int:
        with self._db.session() as db:
            existing_user = db.scalars(
                    select(User).where(User.username == username)
                ).first()
            
            if existing_user is not None:
                raise UserExistsError(username)

            new_user = User(
                username=username,
                password_hash=self._hash_password(password),
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
        with self._db.session() as db:
            user = db.scalar(
                select(User)
                .where(User.id == id)
                .options(
                    joinedload(User.allowed_actions),
                    joinedload(User.allowed_triggers)
                )
            )

            if user is None:
                raise NonexistentUserError(id)

            return user
    
    def get_user_by_name(self, username: str) -> User:
        with self._db.session() as db:
            user = db.scalar(
                select(User).where(User.username == username)
            )

            if user is None:
                raise NonexistentUserError(username)
            
            return user
    
    def delete_user_by_id(self, id: int):
        with self._db.session() as db:
            user = db.scalar(
                select(User).where(User.id == id)
            )

            if user is None:
                raise NonexistentUserError(id)
            
            db.delete(user)
            db.commit()

    def _hash_password(self, password: str) -> str:
        return hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')

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
