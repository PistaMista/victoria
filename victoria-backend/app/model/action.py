from sqlalchemy import Text, String, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.model import Base
from typing import List
from app.model.allowed_agent_action import allowed_agent_action_association
from app.model.allowed_chat_action import allowed_chat_action_association
from app.model.allowed_user_action import allowed_user_action_association

class Action(Base):
    __tablename__ = "action"

    id: Mapped[int] = mapped_column(primary_key=True)
    function_name: Mapped[str] = mapped_column(String(80), nullable=False)
    function_param_schema: Mapped[str] = mapped_column(JSON, nullable=False)
    function_source_code: Mapped[str] = mapped_column(Text(), nullable=False)
    function_docstring: Mapped[str] = mapped_column(Text(), nullable=False)
    
    repository_id: Mapped[int] = mapped_column(ForeignKey("action_repository.id", ondelete='CASCADE'), nullable=False)
    repository: Mapped["ActionRepository"] = relationship("ActionRepository", back_populates="actions")

    allowed_on_agents: Mapped[List["Agent"]] = relationship("Agent", secondary=allowed_agent_action_association, back_populates="allowed_actions")
    allowed_on_chats: Mapped[List["Chat"]] = relationship("Chat", secondary=allowed_chat_action_association, back_populates="allowed_actions")
    allowed_on_users: Mapped[List["User"]] = relationship("User", secondary=allowed_user_action_association, back_populates="allowed_actions")
