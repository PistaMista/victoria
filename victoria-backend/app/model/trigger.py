from app.model import Base
from app.model.allowed_agent_trigger import allowed_agent_trigger_association
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Integer

class Trigger(Base):
    __tablename__ = "trigger"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    type: Mapped[str] = mapped_column(String(10), nullable=False)
    template: Mapped[str] = mapped_column(Text(), nullable=False)
    spawned_events: Mapped[List["Event"]] = relationship("Event", back_populates="trigger")
    allowed_on_agents: Mapped[List["Agent"]] = relationship("Agent", secondary=allowed_agent_trigger_association, back_populates="allowed_triggers")

    __mapper_args__ = {
        'polymorphic_identity': 'NONE',
        'polymorphic_on': type
    }

class PollTrigger(Trigger):
    url: Mapped[str] = mapped_column(String(300), nullable=False)
    interval: Mapped[int] = mapped_column(Integer(), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'POLL'
    }

class ChatTrigger(Trigger):
    receiver: Mapped[str] = mapped_column(String(50), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'CHAT'
    }

class WebhookTrigger(Trigger):
    endpoint: Mapped[str] = mapped_column(String(70), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'WEBHOOK'
    }

class TimerTrigger(Trigger):
    interval: Mapped[int] = mapped_column(Integer(), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'TIMER'
    }