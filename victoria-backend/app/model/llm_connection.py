from app.model import Base
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import mapped_column, relationship, Mapped
from typing import List


class LLMConnection(Base):
    __tablename__ = "llm_connection"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    type: Mapped[str] = mapped_column(String(10), nullable=False)

    models: Mapped[List["LanguageModel"]] = relationship(
        "LanguageModel", back_populates="connection", cascade="all,delete"
    )

    __mapper_args__ = {"polymorphic_identity": "NONE", "polymorphic_on": type}


class OllamaConnection(LLMConnection):
    __tablename__ = "llm_connection_ollama"
    id: Mapped[int] = mapped_column(ForeignKey("llm_connection.id"), primary_key=True)
    url: Mapped[str] = mapped_column(String(300), nullable=False)

    __mapper_args__ = {"polymorphic_identity": "OLLAMA"}
