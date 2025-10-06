from sqlalchemy import String, Text, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.model import Base
from app.model.allowed_agent_trigger import allowed_agent_trigger_association
from app.model.allowed_agent_action import allowed_agent_action_association
from typing import List, Dict, Any

class Agent(Base):
    __tablename__ = "agent"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    prompt: Mapped[str] = mapped_column(Text(), nullable=False)

    owner_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete='CASCADE'), nullable=False)
    owner: Mapped["User"] = relationship("User", back_populates="agents")
    
    model_id: Mapped[int] = mapped_column(ForeignKey("language_model.id"), nullable=True)
    model: Mapped["LanguageModel"] = relationship("LanguageModel")

    model_params: Mapped[Dict[str, Any]] = mapped_column(JSON(), nullable=False, default={})
    
    allowed_triggers: Mapped[List["Trigger"]] = relationship("Trigger", secondary=allowed_agent_trigger_association, back_populates="allowed_on_agents")
    allowed_actions: Mapped[List["Action"]] = relationship("Action", secondary=allowed_agent_action_association, back_populates="allowed_on_agents")
    monologues: Mapped[List["Monologue"]] = relationship("Monologue", back_populates="agent")
