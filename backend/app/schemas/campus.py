from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, field_validator


def normalizar_instante_utc(instante: datetime | None) -> datetime | None:
    """Mantém o contrato com fuso mesmo quando o SQLite de testes remove o offset."""
    if instante is not None and (instante.tzinfo is None or instante.utcoffset() is None):
        return instante.replace(tzinfo=UTC)
    return instante


class CampusRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    ultima_importacao_em: datetime | None = None
    ultima_fonte_pdf_url: str | None = None

    _normalizar_instante = field_validator("ultima_importacao_em", mode="before")(
        normalizar_instante_utc
    )
