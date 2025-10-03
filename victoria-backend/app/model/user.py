import enum
from app.model import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Enum
from typing import List
from app.model.allowed_user_action import allowed_user_action_association
from app.model.allowed_user_trigger import allowed_user_trigger_association

class Role(enum.Enum):
    USER = 0
    ADMIN = 1
    
    def __str__(self):
        return self.name.lower()

class User(Base):
    __tablename__ = "user"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    role: Mapped[Role] = mapped_column(Enum(Role, native_enum=False), nullable=False)

    chats: Mapped[List["Chat"]] = relationship("Chat", back_populates="owner", cascade='all,delete', order_by="Chat.modified_at.desc()")

    allowed_actions: Mapped[List["Action"]] = relationship("Action", secondary=allowed_user_action_association, back_populates="allowed_on_users")
    allowed_triggers: Mapped[List["Trigger"]] = relationship("Trigger", secondary=allowed_user_trigger_association, back_populates="allowed_on_users")
    
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.id!r})"
