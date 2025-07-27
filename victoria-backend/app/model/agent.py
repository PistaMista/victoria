from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.model import Base
from app.model.allowed_agent_trigger import allowed_agent_trigger_association

class Agent(Base):
    __tablename__ = "agent"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    prompt: Mapped[str] = mapped_column(Text(), nullable=False)
    
    allowed_triggers: Mapped[List["Trigger"]] = relationship("Trigger", secondary=allowed_agent_trigger_association, back_populates="allowed_on_agents")
    monologues: Mapped[List["Monologue"]] = relationship("Monologue", back_populates="monologues")