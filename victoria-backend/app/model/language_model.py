from app.model import Base
from sqlalchemy.orm import mapped_column, relationship, Mapped
from sqlalchemy import ForeignKey, String, Boolean

class LanguageModel(Base):
    __tablename__ = "language_model"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(400), nullable=False)
    enabled: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    
    # The connection the model was imported from
    connection_id: Mapped[int] = mapped_column(ForeignKey("llm_connection.id", ondelete='CASCADE'), nullable=False)
    connection: Mapped["LLMConnection"] = relationship("LLMConnection", back_populates="models")
