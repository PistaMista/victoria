import enum
from sqlalchemy import String, ForeignKey, Enum, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.model import Base
from typing import List, Dict, Any, Literal

class MonologueStatus(enum.Enum):
    PENDING = 0
    RUNNING = 1
    SUCCESS = 2
    FAILURE = 3
    
    def to_status_str(self) -> Literal["PENDING", "RUNNING", "SUCCESS", "FAILURE"]:
        return self.name
                

class Monologue(Base):
    __tablename__ = "monologue"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(80), nullable=True)
    summary: Mapped[str] = mapped_column(String(120), nullable=True)
    status: Mapped[MonologueStatus] = mapped_column(Enum(MonologueStatus, native_enum=False), nullable=False)
    context: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=True)

    event_id: Mapped[int] = mapped_column(ForeignKey("event.id"), nullable=False)
    event: Mapped["Event"] = relationship("Event", back_populates="monologues")
    
    agent_id: Mapped[int] = mapped_column(ForeignKey("agent.id"), nullable=False)
    agent: Mapped["Agent"] = relationship("Agent", back_populates="monologues")
    
    thoughts: Mapped[List["Thought"]] = relationship("Thought", back_populates="monologue", order_by="Thought.timestamp")
    
    def is_finished(self):
        return self.status in [MonologueStatus.SUCCESS, MonologueStatus.FAILURE]
