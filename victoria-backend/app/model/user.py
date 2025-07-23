import enum
from app.model import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Enum

class Role(enum.Enum):
    USER = 0
    ADMIN = 1
    
    def __str__(self):
        return self.name.lower()

class User(Base):
    __tablename__ = "user"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    role: Mapped[Role] = mapped_column(Enum(Role, native_enum=False), nullable=False)
    
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.id!r})"