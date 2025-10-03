from app.model import Base
from sqlalchemy import ForeignKey, String, DateTime, Text, JSON
from sqlalchemy.orm import mapped_column, relationship, Mapped
from datetime import datetime
from typing import List, Any

class ChatMessage(Base):
    __tablename__ = "chat_message"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String(10), nullable=False)

    timestamp: Mapped[datetime] = mapped_column(DateTime(), nullable=False)

    usermsg_exchange_id: Mapped[int] = mapped_column(ForeignKey("chat_exchange.id", ondelete='CASCADE'), nullable=True, unique=True)
    usermsg_exchange: Mapped["ChatExchange"] = relationship(
            "ChatExchange",
            back_populates="user_message",
            foreign_keys=[usermsg_exchange_id]
        )

    reply_exchange_id: Mapped[int] = mapped_column(ForeignKey("chat_exchange.id", ondelete='CASCADE'), nullable=True)
    reply_exchange: Mapped["ChatExchange"] = relationship(
            "ChatExchange",
            back_populates="agent_replies",
            foreign_keys=[reply_exchange_id]
        )

    sending_agent_id: Mapped[int] = mapped_column(ForeignKey("agent.id"), nullable=True)
    sending_agent: Mapped["Agent"] = relationship("Agent")

    sending_user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=True)
    sending_user: Mapped["User"] = relationship("User")

    __mapper_args__ = {
        'polymorphic_identity': 'NONE',
        'polymorphic_on': type
    }

class ChatMessageMarkdown(ChatMessage):
    __tablename__ = "chat_message_markdown"

    id: Mapped[int] = mapped_column(ForeignKey('chat_message.id'), primary_key=True)
    markdown: Mapped[str] = mapped_column(Text(), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'MARKDOWN'
    }

class ChatMessageChoicePrompt(ChatMessage):
    __tablename__ = "chat_message_prompt"

    id: Mapped[int] = mapped_column(ForeignKey('chat_message.id'), primary_key=True)

    prompt: Mapped[str] = mapped_column(String(120), nullable=False)
    choices: Mapped[List["ChoiceMessageOption"]] = relationship(
            "ChoiceMessageOption",
            back_populates="message",
            cascade='all,delete'
        )

    __mapper_args__ = {
        'polymorphic_identity': 'CHOICE'
    }

class ChoiceMessageOption(Base):
    __tablename__ = "chat_message_prompt_option"

    id: Mapped[int] = mapped_column(primary_key=True)
    message_id: Mapped[int] = mapped_column(ForeignKey('chat_message_prompt.id', ondelete='CASCADE'), nullable=False)
    message: Mapped[ChatMessageChoicePrompt] = relationship("ChatMessageChoicePrompt", back_populates="choices")
    value: Mapped[Any] = mapped_column(JSON(), nullable=False)
