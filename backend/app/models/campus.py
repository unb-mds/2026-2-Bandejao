from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base

# As relações são resolvidas pelo SQLAlchemy pelo nome; os imports servem só à tipagem.
if TYPE_CHECKING:
    from app.models.cardapio import Cardapio
    from app.models.checkin import CheckIn


class Campus(Base):
    __tablename__ = "campus"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    ultima_importacao_em: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    ultima_fonte_pdf_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    cardapios: Mapped[list["Cardapio"]] = relationship(
        back_populates="campus", cascade="all, delete-orphan"
    )
    checkins: Mapped[list["CheckIn"]] = relationship(
        back_populates="campus", cascade="all, delete-orphan"
    )
