from sqlalchemy import Text, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.model import Base

class Invocation(Base):
    __tablename__ = "invocation"

    id: Mapped[int] = mapped_column(primary_key=True)
    thought: Mapped["Thought"] = relationship("Thought", back_populates="invocation")
    type: Mapped[str] = mapped_column(String(10), nullable=False)
    
    __mapper_args__ = {
        'polymorphic_identity': 'NONE',
        'polymorphic_on': type
    }

class TriggerInvocation(Invocation):
    __tablename__ = "invocation_trigger"

    id: Mapped[int] = mapped_column(ForeignKey('invocation.id'), primary_key=True)

    event_id: Mapped[int] = mapped_column(ForeignKey("event.id"), nullable=False)
    event: Mapped["Event"] = relationship("Event")
    
    __mapper_args__ = {
        'polymorphic_identity': 'TRIGGER'
    }

class ThoughtInvocation(Invocation):
    __tablename__ = "invocation_thought"

    id: Mapped[int] = mapped_column(ForeignKey('invocation.id'), primary_key=True)

    content: Mapped[str] = mapped_column(Text(), nullable=False)
    
    __mapper_args__ = {
        'polymorphic_identity': 'THOUGHT'
    }

class ActionInvocation(Invocation):
    __tablename__ = "invocation_action"

    id: Mapped[int] = mapped_column(ForeignKey('invocation.id'), primary_key=True)
    
    function_name: Mapped[str] = mapped_column(String(60), nullable=False)
    param_json: Mapped[str] = mapped_column(Text(), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'ACTION'
    }

class SuccessInvocation(Invocation):
    __tablename__ = "invocation_success"

    id: Mapped[int] = mapped_column(ForeignKey('invocation.id'), primary_key=True)
    reason: Mapped[str] = mapped_column(Text(), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'SUCCESS'
    }

class FailureInvocation(Invocation):
    __tablename__ = "invocation_failure"

    id: Mapped[int] = mapped_column(ForeignKey('invocation.id'), primary_key=True)
    reason: Mapped[str] = mapped_column(Text(), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'FAILURE'
    }
    