from app.model import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Integer, ForeignKey, Boolean
from typing import List

class Event(Base):
    __tablename__ = "event"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String(10), nullable=False)
    trigger_id: Mapped[int] = mapped_column(ForeignKey("trigger.id"), nullable=True)
    trigger: Mapped["Trigger"] = relationship(back_populates="spawned_events")
    content: Mapped[str] = mapped_column(Text(), nullable=False)
    dispatched: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    monologues: Mapped[List["Monologue"]] = relationship("Monologue", back_populates="event")

    __mapper_args__ = {
        'polymorphic_identity': 'BASE',
        'polymorphic_on': type
    }


class ChatEvent(Event):
    __tablename__ = "event_chat"

    id: Mapped[int] = mapped_column(ForeignKey("event.id"), primary_key=True)

    triggering_chat_exchange_id: Mapped[int] = mapped_column(ForeignKey("chat_exchange.id"), nullable=True)
    triggering_chat_exchange: Mapped["ChatExchange"] = relationship("ChatExchange", back_populates="triggered_chat_events")

    __mapper_args__ = {
        'polymorphic_identity': 'CHAT'
    }

