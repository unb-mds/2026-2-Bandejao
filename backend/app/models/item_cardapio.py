from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base
from app.models.enums import Categoria, TipoDieta

# Evita importar Cardapio durante a execução apenas para satisfazer a tipagem.
if TYPE_CHECKING:
    from app.models.cardapio import Cardapio


class ItemCardapio(Base):
    __tablename__ = "item_cardapio"

    id: Mapped[int] = mapped_column(primary_key=True)
    cardapio_id: Mapped[int] = mapped_column(
        ForeignKey("cardapio.id", ondelete="CASCADE"), nullable=False
    )
    categoria: Mapped[Categoria] = mapped_column(
        Enum(Categoria, name="categoria"), nullable=False
    )
    tipo_dieta: Mapped[TipoDieta] = mapped_column(
        Enum(TipoDieta, name="tipo_dieta"), nullable=False, default=TipoDieta.COMUM
    )
    nome: Mapped[str] = mapped_column(String(200), nullable=False)

    # Alérgenos, conforme legenda do cardápio do RU
    contem_leite: Mapped[bool] = mapped_column(Boolean, default=False)
    contem_ovo: Mapped[bool] = mapped_column(Boolean, default=False)
    contem_gluten: Mapped[bool] = mapped_column(Boolean, default=False)
    contem_cogumelo: Mapped[bool] = mapped_column(Boolean, default=False)
    contem_amendoim: Mapped[bool] = mapped_column(Boolean, default=False)
    contem_mel: Mapped[bool] = mapped_column(Boolean, default=False)
    contem_soja: Mapped[bool] = mapped_column(Boolean, default=False)
    contem_pimenta: Mapped[bool] = mapped_column(Boolean, default=False)
    contem_oleaginosas: Mapped[bool] = mapped_column(Boolean, default=False)
    contem_carne_suina: Mapped[bool] = mapped_column(Boolean, default=False)
    contem_frutos_do_mar: Mapped[bool] = mapped_column(Boolean, default=False)

    cardapio: Mapped["Cardapio"] = relationship(back_populates="itens")
