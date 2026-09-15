from pydantic import BaseModel, ConfigDict

from app.models.enums import Categoria, TipoDieta


class ItemCardapioRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    categoria: Categoria
    tipo_dieta: TipoDieta
    nome: str
    contem_leite: bool
    contem_ovo: bool
    contem_gluten: bool
    contem_cogumelo: bool
    contem_mel: bool
    contem_soja: bool
    contem_pimenta: bool
    contem_oleaginosas: bool
    contem_carne_suina: bool
    contem_frutos_do_mar: bool
