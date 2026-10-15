from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Header, HTTPException, Response
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.avaliacao import Avaliacao
from app.models.cardapio import Cardapio
from app.schemas.avaliacao import AvaliacaoCreate, AvaliacaoRead

router = APIRouter(prefix="/cardapios/{cardapio_id}/avaliacoes", tags=["avaliacao"])


def _obter_cardapio_ou_404(cardapio_id: int, db: Session) -> None:
    if db.get(Cardapio, cardapio_id) is None:
        raise HTTPException(status_code=404, detail="Cardápio não encontrado")


def _obter_identidade(
    x_identidade: Annotated[str | None, Header(alias="X-Identidade")] = None,
) -> UUID:
    try:
        identidade = UUID(x_identidade) if x_identidade else None
    except (ValueError, AttributeError):
        identidade = None
    if identidade is None or identidade.version != 4:
        raise HTTPException(
            status_code=400,
            detail="O cabeçalho X-Identidade deve conter um UUID v4 válido",
        )
    return identidade


@router.get("/", response_model=list[AvaliacaoRead])
def listar_avaliacoes(cardapio_id: int, db: Session = Depends(get_db)):
    _obter_cardapio_ou_404(cardapio_id, db)
    return (
        db.query(Avaliacao)
        .filter(Avaliacao.cardapio_id == cardapio_id)
        .order_by(Avaliacao.criado_em.desc())
        .all()
    )


@router.post("/", response_model=AvaliacaoRead, status_code=201)
def criar_avaliacao(
    cardapio_id: int,
    payload: AvaliacaoCreate,
    response: Response,
    identidade: Annotated[UUID, Depends(_obter_identidade)],
    db: Session = Depends(get_db),
):
    _obter_cardapio_ou_404(cardapio_id, db)
    avaliacao = (
        db.query(Avaliacao)
        .filter(
            Avaliacao.cardapio_id == cardapio_id,
            Avaliacao.identidade == identidade,
        )
        .one_or_none()
    )
    if avaliacao is None:
        avaliacao = Avaliacao(
            cardapio_id=cardapio_id,
            identidade=identidade,
            **payload.model_dump(),
        )
        db.add(avaliacao)
    else:
        avaliacao.nota = payload.nota
        avaliacao.comentario = payload.comentario
        response.status_code = 200
    db.commit()
    db.refresh(avaliacao)
    return avaliacao
