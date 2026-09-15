from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AvaliacaoCreate(BaseModel):
    nota: int = Field(ge=1, le=5)
    comentario: str | None = Field(default=None, max_length=500)


class AvaliacaoRead(AvaliacaoCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    cardapio_id: int
    criado_em: datetime
