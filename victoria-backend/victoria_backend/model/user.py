from victoria_backend.model import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

class User(Base):
    __tablename__ = "user"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.id!r})"