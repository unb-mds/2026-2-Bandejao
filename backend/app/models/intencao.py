from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Boolean, ForeignKey, UniqueConstraint, Uuid, false, true
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base

if TYPE_CHECKING:
    from app.models.cardapio import Cardapio


class Intencao(Base):
    """Estado único de intenção por refeição e identidade, preservado no cancelamento."""

    __tablename__ = "intencao"
    __table_args__ = (
        UniqueConstraint("cardapio_id", "identidade", name="uq_intencao_cardapio_identidade"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    cardapio_id: Mapped[int] = mapped_column(
        ForeignKey("cardapio.id", ondelete="CASCADE"), nullable=False
    )
    identidade: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    ativa: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default=true())
    simulada: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default=false()
    )

    cardapio: Mapped["Cardapio"] = relationship(back_populates="intencoes")
