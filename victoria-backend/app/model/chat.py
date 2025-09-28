from app.model import Base
from app.model.allowed_chat_action import allowed_chat_action_association
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, ForeignKey, DateTime
from datetime import datetime
from typing import List

class Chat(Base):
    __tablename__ = "chat"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(60), nullable=False)
    summary: Mapped[str] = mapped_column(String(180), nullable=False)
    receiver: Mapped[str] = mapped_column(String(30), nullable=False)

    owner_id: Mapped[str] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    owner: Mapped["User"] = relationship("User", back_populates="chats")

    exchanges: Mapped[List["ChatExchange"]] = relationship("ChatExchange", back_populates="chat", cascade="all,delete", order_by="ChatExchange.timestamp.asc()")

    created_at: Mapped[datetime] = mapped_column(DateTime(), nullable=False)
    modified_at: Mapped[datetime] = mapped_column(DateTime(), nullable=False)

    allowed_actions: Mapped[List["Action"]] = relationship("Action", secondary=allowed_chat_action_association, back_populates="allowed_on_chats")


