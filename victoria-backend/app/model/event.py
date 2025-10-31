from app.model import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Integer, ForeignKey, Boolean
from typing import List

class Event(Base):
    __tablename__ = "event"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    trigger_id: Mapped[int] = mapped_column(ForeignKey("trigger.id"), nullable=True)
    trigger: Mapped["Trigger"] = relationship(back_populates="spawned_events")
    content: Mapped[str] = mapped_column(Text(), nullable=False)
    dispatched: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    monologues: Mapped[List["Monologue"]] = relationship("Monologue", back_populates="event")

    triggering_chat_exchange_id: Mapped[int] = mapped_column(ForeignKey("chat_exchange.id"), nullable=True)
    triggering_chat_exchange: Mapped["ChatExchange"] = relationship("ChatExchange", back_populates="triggered_chat_events")
