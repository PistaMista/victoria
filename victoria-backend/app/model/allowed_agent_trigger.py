from sqlalchemy import Column, Table, ForeignKey
from app.model import Base

allowed_agent_trigger_association = Table(
    "allowed_agent_trigger",
    Base.metadata,
    Column("agent_id", ForeignKey("agent.id", ondelete='CASCADE'), nullable=False),
    Column("trigger_id", ForeignKey("trigger.id", ondelete='CASCADE'), nullable=False)
)
