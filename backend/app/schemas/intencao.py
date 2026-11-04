from datetime import date

from pydantic import BaseModel

from app.models.enums import TipoRefeicao


class IntencaoRead(BaseModel):
    cardapio_id: int
    ativa: bool


class IntencaoPessoalRead(IntencaoRead):
    campus_id: int
    data: date
    tipo_refeicao: TipoRefeicao
