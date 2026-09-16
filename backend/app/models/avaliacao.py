from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base

# Importado apenas na análise estática para não criar um ciclo entre modelos em runtime.
if TYPE_CHECKING:
    from app.models.cardapio import Cardapio


class Avaliacao(Base):
    __tablename__ = "avaliacao"
    __table_args__ = (
        CheckConstraint("nota >= 1 AND nota <= 5", name="ck_avaliacao_nota_range"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    cardapio_id: Mapped[int] = mapped_column(
        ForeignKey("cardapio.id", ondelete="CASCADE"), nullable=False
    )
    nota: Mapped[int] = mapped_column(Integer, nullable=False)
    comentario: Mapped[str | None] = mapped_column(String(500), nullable=True)
    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    cardapio: Mapped["Cardapio"] = relationship(back_populates="avaliacoes")
