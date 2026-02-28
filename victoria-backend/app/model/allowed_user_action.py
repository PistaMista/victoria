from sqlalchemy import Column, Table, ForeignKey
from app.model import Base

allowed_user_action_association = Table(
    "allowed_user_action",
    Base.metadata,
    Column(
        "user_id",
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    ),
    Column(
        "action_id",
        ForeignKey("action.id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    ),
)
