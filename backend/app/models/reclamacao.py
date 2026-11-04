from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import DateTime, Enum, ForeignKey, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base
from app.models.enums import CategoriaReclamacao

if TYPE_CHECKING:
    from app.models.cardapio import Cardapio


class Reclamacao(Base):
    """Relato anônimo sobre uma refeição (RF08, D06). Sem nome, foto ou nota."""

    __tablename__ = "reclamacao"

    id: Mapped[int] = mapped_column(primary_key=True)
    cardapio_id: Mapped[int] = mapped_column(
        ForeignKey("cardapio.id", ondelete="CASCADE"), nullable=False
    )
    identidade: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    categoria: Mapped[CategoriaReclamacao] = mapped_column(
        Enum(CategoriaReclamacao, name="categoria_reclamacao"), nullable=False
    )
    descricao: Mapped[str] = mapped_column(String(1000), nullable=False)
    criado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    cardapio: Mapped["Cardapio"] = relationship(back_populates="reclamacoes")
