from sqlalchemy import Text, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.model import Base
from typing import List
from app.model.allowed_agent_action import allowed_agent_action_association

class Action(Base):
    __tablename__ = "action"

    id: Mapped[int] = mapped_column(primary_key=True)
    function_name: Mapped[str] = mapped_column(String(80), nullable=False)
    allowed_on_agents: Mapped[List["Agent"]] = relationship("Agent", secondary=allowed_agent_action_association, back_populates="allowed_actions")