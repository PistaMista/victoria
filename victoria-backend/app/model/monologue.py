import enum
from sqlalchemy import String, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.model import Base

class MonologueStatus(enum.Enum):
    PENDING = 0
    RUNNING = 1
    SUCCESS = 2
    FAILURE = 3

class Monologue(Base):
    __tablename__ = "monologue"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(80), nullable=True)
    summary: Mapped[str] = mapped_column(String(120), nullable=True)
    status: Mapped[MonologueStatus] = mapped_column(Enum(MonologueStatus, native_enum=False), nullable=False)

    event_id: Mapped[int] = mapped_column(ForeignKey("event.id"), nullable=False)
    event: Mapped["Event"] = relationship("Event", back_populates="monologues")
    
    agent_id: Mapped[int] = mapped_column(ForeignKey("agent.id"), nullable=False)
    agent: Mapped["Agent"] = relationship("Agent", back_populates="monologues")
    
    # thoughts: Mapped[List["Thought"]] = relationship("Thought", back_populates="monologue")
    
