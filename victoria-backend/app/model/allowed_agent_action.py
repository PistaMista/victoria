from sqlalchemy import Column, Table, ForeignKey
from app.model import Base

allowed_agent_action_association = Table(
    "allowed_agent_action",
    Base.metadata,
    Column(
        "agent_id",
        ForeignKey("agent.id", ondelete="CASCADE"),
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
