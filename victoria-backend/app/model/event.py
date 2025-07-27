from app.model import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Integer, ForeignKey, Boolean

class Event(Base):
    __tablename__ = "event"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    trigger_id: Mapped[int] = mapped_column(ForeignKey("trigger.id"), nullable=False)
    trigger: Mapped["Trigger"] = relationship(back_populates="spawned_events")
    content: Mapped[str] = mapped_column(Text(), nullable=False)
    dispatched: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    monologues: Mapped[List["Monologue"]] = relationship("Monologue", back_populates="event")