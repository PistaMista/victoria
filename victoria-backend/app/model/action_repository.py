from sqlalchemy import String
from sqlalchemy.orm import mapped_column, relationship, Mapped
from app.model import Base
from typing import List


class ActionRepository(Base):
    __tablename__ = "action_repository"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    url: Mapped[str] = mapped_column(String(300), nullable=False)
    
    actions: Mapped[List["Action"]] = relationship("Action", back_populates="repository")