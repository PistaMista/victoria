from app.model import Base
from sqlalchemy.orm import mapped_column, relationship, Mapped
from sqlalchemy import ForeignKey, String

class LanguageModel(Base):
    __tablename__ = "language_model"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    
    # The connection the model was imported from
    connection_id: Mapped[int] = mapped_column(ForeignKey("llm_connection.id"), nullable=False)
    connection: Mapped["Connection"] = relationship("Connection", back_populates="models")