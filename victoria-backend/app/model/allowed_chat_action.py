from sqlalchemy import Column, Table, ForeignKey
from app.model import Base

allowed_chat_action_association = Table(
    "allowed_chat_action",
    Base.metadata,
    Column("chat_id", ForeignKey("chat.id", ondelete='CASCADE'), nullable=False),
    Column("action_id", ForeignKey("action.id", ondelete='CASCADE'), nullable=False)
)
