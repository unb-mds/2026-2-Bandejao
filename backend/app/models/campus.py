from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Campus(Base):
    __tablename__ = "campus"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    cardapios: Mapped[list["Cardapio"]] = relationship(
        back_populates="campus", cascade="all, delete-orphan"
    )
    checkins: Mapped[list["CheckIn"]] = relationship(
        back_populates="campus", cascade="all, delete-orphan"
    )
