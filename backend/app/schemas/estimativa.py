from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, Field

from app.models.enums import TipoRefeicao


class EstimativaRead(BaseModel):
    cardapio_id: int
    campus_id: int
    data: date
    tipo_refeicao: TipoRefeicao
    data_inicio: date
    data_fim: date
    calculado_em: datetime
    dados_simulados: bool
    amostra_minima: int
    status: Literal["dados_insuficientes", "disponivel"]
    mensagem: str
    contagem: int | None = Field(default=None, ge=0)
