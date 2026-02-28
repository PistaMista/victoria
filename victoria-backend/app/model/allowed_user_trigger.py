from sqlalchemy import Column, Table, ForeignKey
from app.model import Base

allowed_user_trigger_association = Table(
    "allowed_user_trigger",
    Base.metadata,
    Column(
        "user_id",
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    ),
    Column(
        "trigger_id",
        ForeignKey("trigger.id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    ),
)
