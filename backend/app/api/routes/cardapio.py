from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, selectinload

from app.db.session import get_db
from app.models.cardapio import Cardapio
from app.models.enums import TipoDieta, TipoRefeicao
from app.schemas.cardapio import CardapioRead

router = APIRouter(prefix="/cardapios", tags=["cardapio"])

# Alérgenos que podem ser excluídos via filtro, mapeados para o campo do model
ALERGENOS_VALIDOS = {
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


@router.get("/", response_model=list[CardapioRead])
def listar_cardapios(
    campus_id: int | None = Query(default=None),
    data_inicio: date | None = Query(default=None),
    data_fim: date | None = Query(default=None),
    tipo_refeicao: TipoRefeicao | None = Query(default=None),
    tipo_dieta: TipoDieta | None = Query(
        default=None, description="Restringe os itens retornados a esta dieta"
    ),
    excluir_alergenos: list[str] | None = Query(
        default=None,
        description=f"Alérgenos a excluir dos itens. Opções: {', '.join(sorted(ALERGENOS_VALIDOS))}",
    ),
    db: Session = Depends(get_db),
) -> list[CardapioRead]:
    for alergeno in excluir_alergenos or []:
        if alergeno not in ALERGENOS_VALIDOS:
            raise HTTPException(
                status_code=400,
                detail=f"Alérgeno inválido: {alergeno}. Opções: {', '.join(sorted(ALERGENOS_VALIDOS))}",
            )

    query = db.query(Cardapio).options(selectinload(Cardapio.itens))
    if campus_id is not None:
        query = query.filter(Cardapio.campus_id == campus_id)
    if data_inicio is not None:
        query = query.filter(Cardapio.data >= data_inicio)
    if data_fim is not None:
        query = query.filter(Cardapio.data <= data_fim)
    if tipo_refeicao is not None:
        query = query.filter(Cardapio.tipo_refeicao == tipo_refeicao)

    cardapios = query.order_by(Cardapio.data).all()
    resultado = [CardapioRead.model_validate(c) for c in cardapios]

    if tipo_dieta is not None or excluir_alergenos:
        for cardapio in resultado:
            itens = cardapio.itens
            if tipo_dieta is not None:
                itens = [i for i in itens if i.tipo_dieta == tipo_dieta]
            for alergeno in excluir_alergenos or []:
                itens = [i for i in itens if not getattr(i, f"contem_{alergeno}")]
            cardapio.itens = itens

    return resultado


@router.get("/{cardapio_id}", response_model=CardapioRead)
def obter_cardapio(cardapio_id: int, db: Session = Depends(get_db)):
    cardapio = (
        db.query(Cardapio)
        .options(selectinload(Cardapio.itens))
        .filter(Cardapio.id == cardapio_id)
        .first()
    )
    if cardapio is None:
        raise HTTPException(status_code=404, detail="Cardápio não encontrado")
    return cardapio
