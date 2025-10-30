from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Text, DateTime
from datetime import datetime
from app.model import Base


class Thought(Base):
    __tablename__ = "thought"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    # If there is no invocation assigned, it means that this Thought is not a result of the Agent's actions (e.g. comes from a Trigger)
    invocation_id: Mapped[int] = mapped_column(ForeignKey("invocation.id"), nullable=True)
    invocation: Mapped["Invocation"] = relationship("Invocation", back_populates="thought")
    monologue_id: Mapped[int] = mapped_column(ForeignKey("monologue.id"), nullable=False)
    monologue: Mapped["Monologue"] = relationship("Monologue", back_populates="thoughts")
    result: Mapped[str] = mapped_column(Text(), nullable=True)
