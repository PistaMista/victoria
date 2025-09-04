from sqlalchemy import Text, String, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.model import Base
from typing import Dict, Any

class Invocation(Base):
    __tablename__ = "invocation"

    id: Mapped[int] = mapped_column(primary_key=True)
    thought: Mapped["Thought"] = relationship("Thought", back_populates="invocation")
    
    action_id: Mapped[int] = mapped_column(ForeignKey("action.id"), nullable=False)
    action: Mapped["Action"] = relationship("Action")
    
    params: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)