from app.services.db import DatabaseService
from bcrypt import hashpw, gensalt
from typing import Optional
from app.model.user import User, Role
from sqlalchemy import select, delete

class UserService:
    def __init__(self, db_service: DatabaseService):
        self._db = db_service
        
    def create_user(self, username: str, password: str, role: Role) -> None:
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
            db.add(new_user)
            db.commit()
    
    def is_any_user_registered(self) -> bool:
        with self._db.session() as db:
            first_user = db.scalars(
                select(User)
            ).first()

            return first_user is not None

    def get_user_by_id(self, id: int) -> Optional[User]:
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

class UserExistsError(Exception):
    def __init__(self, username: str):
        super().__init__(f"user {username} already exists")