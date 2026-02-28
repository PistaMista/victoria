from sqlalchemy import Text, String, ForeignKey, JSON, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.model import Base
from typing import Dict, Any


class Invocation(Base):
    __tablename__ = "invocation"

    id: Mapped[int] = mapped_column(primary_key=True)
    thought: Mapped["Thought"] = relationship("Thought", back_populates="invocation")

    # If action_id is null, then this Invocation was not recognized as a valid action
    action_id: Mapped[int] = mapped_column(ForeignKey("action.id"), nullable=True)
    action: Mapped["Action"] = relationship("Action")

    # If function_name or params are null, they could not be parsed from the generated response
    function_name: Mapped[str] = mapped_column(String(80), nullable=True)
    params: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=True)

    function_name_semantically_valid: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    params_semantically_valid: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
