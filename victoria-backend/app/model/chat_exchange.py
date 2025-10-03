from app.model import Base
from app.model.chat_message import ChatMessage
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import mapped_column, relationship, Mapped
from datetime import datetime
from typing import List

class ChatExchange(Base):
    __tablename__ = "chat_exchange"
    
    id: Mapped[int] = mapped_column(primary_key=True)

    timestamp: Mapped[datetime] = mapped_column(DateTime(), nullable=False)

    user_message: Mapped["ChatMessage"] = relationship(
            "ChatMessage",
            back_populates="usermsg_exchange",
            foreign_keys=[ChatMessage.usermsg_exchange_id],
            cascade="all,delete"
        )
    agent_replies: Mapped[List["ChatMessage"]] = relationship(
            "ChatMessage",
            back_populates="reply_exchange",
            foreign_keys=[ChatMessage.reply_exchange_id],
            cascade="all,delete"
        )

    chat_id: Mapped[int] = mapped_column(ForeignKey("chat.id", ondelete='CASCADE'), nullable=False)
    chat: Mapped["Chat"] = relationship("Chat", back_populates="exchanges")

    triggered_chat_events: Mapped[List["ChatEvent"]] = relationship("ChatEvent", back_populates="triggering_chat_exchange")
