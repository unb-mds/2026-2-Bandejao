from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class CheckIn(Base):
    """Registro de check-in de um usuário em um campus (Release 2).

    Usado para estimar horários de pico de fila a partir do histórico.
    """

    __tablename__ = "checkin"

    id: Mapped[int] = mapped_column(primary_key=True)
    campus_id: Mapped[int] = mapped_column(
        ForeignKey("campus.id", ondelete="CASCADE"), nullable=False
    )
    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    campus: Mapped["Campus"] = relationship(back_populates="checkins")
