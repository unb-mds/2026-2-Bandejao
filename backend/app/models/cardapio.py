from datetime import date as date_type
from typing import TYPE_CHECKING

from sqlalchemy import Date, Enum, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base
from app.models.enums import TipoRefeicao

# Mantém as anotações das relações sem importar modelos mutuamente em runtime.
if TYPE_CHECKING:
    from app.models.avaliacao import Avaliacao
    from app.models.campus import Campus
    from app.models.item_cardapio import ItemCardapio


class Cardapio(Base):
    __tablename__ = "cardapio"
    __table_args__ = (
        UniqueConstraint(
            "campus_id", "data", "tipo_refeicao", name="uq_cardapio_campus_data_tipo"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    campus_id: Mapped[int] = mapped_column(
        ForeignKey("campus.id", ondelete="CASCADE"), nullable=False
    )
    data: Mapped[date_type] = mapped_column(Date, nullable=False)
    tipo_refeicao: Mapped[TipoRefeicao] = mapped_column(
        Enum(TipoRefeicao, name="tipo_refeicao"), nullable=False
    )
    fonte_pdf_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    campus: Mapped["Campus"] = relationship(back_populates="cardapios")
    itens: Mapped[list["ItemCardapio"]] = relationship(
        back_populates="cardapio", cascade="all, delete-orphan"
    )
    avaliacoes: Mapped[list["Avaliacao"]] = relationship(
        back_populates="cardapio", cascade="all, delete-orphan"
    )
