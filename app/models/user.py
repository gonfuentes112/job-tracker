from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .application import Application


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[String] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[String] = mapped_column(String(255))
    applications: Mapped[list["Application"]] = relationship(back_populates="user")
