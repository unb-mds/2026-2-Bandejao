from datetime import date

from pydantic import BaseModel, ConfigDict

from app.models.enums import TipoRefeicao
from app.schemas.item_cardapio import ItemCardapioRead


class CardapioRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    campus_id: int
    data: date
    tipo_refeicao: TipoRefeicao
    fonte_pdf_url: str | None
    itens: list[ItemCardapioRead] = []
