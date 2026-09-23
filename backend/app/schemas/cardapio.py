from datetime import date

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.enums import Categoria, TipoDieta, TipoRefeicao
from app.schemas.item_cardapio import ItemCardapioRead

ALERGENOS_VALIDOS = frozenset(
    {
        "leite",
        "ovo",
        "gluten",
        "cogumelo",
        "mel",
        "soja",
        "pimenta",
        "oleaginosas",
        "carne_suina",
        "frutos_do_mar",
    }
)


class CardapioRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    campus_id: int
    data: date
    tipo_refeicao: TipoRefeicao
    fonte_pdf_url: str | None
    itens: list[ItemCardapioRead] = []


class ItemCardapioImportacao(BaseModel):
    """Representa um item já normalizado pela etapa de extração."""

    categoria: Categoria
    tipo_dieta: TipoDieta
    nome: str = Field(min_length=1, max_length=200)
    alergenos: set[str] = Field(default_factory=set)

    @field_validator("alergenos")
    @classmethod
    def validar_alergenos(cls, alergenos: set[str]) -> set[str]:
        desconhecidos = alergenos - ALERGENOS_VALIDOS
        if desconhecidos:
            raise ValueError(
                f"Alérgenos inválidos: {', '.join(sorted(desconhecidos))}. "
                f"Opções: {', '.join(sorted(ALERGENOS_VALIDOS))}"
            )
        return alergenos


class RefeicaoImportacao(BaseModel):
    data: date
    tipo_refeicao: TipoRefeicao
    itens: list[ItemCardapioImportacao] = Field(default_factory=list)


class CardapioImportacao(BaseModel):
    """Payload interno enviado pela extração para substituir o cardápio semanal."""

    campus: str = Field(min_length=1, max_length=100)
    fonte_pdf_url: str | None = Field(default=None, max_length=500)
    refeicoes: list[RefeicaoImportacao] = Field(default_factory=list)


class ImportacaoResultado(BaseModel):
    campus_id: int
    cardapios_processados: int
    itens_processados: int
