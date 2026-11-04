from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.api.dependencias import exigir_janela_aberta, obter_identidade
from app.core.tempo import agora
from app.db.session import get_db
from app.models.avaliacao import Avaliacao
from app.models.cardapio import Cardapio
from app.schemas.avaliacao import AvaliacaoCreate, AvaliacaoRead

router = APIRouter(prefix="/cardapios/{cardapio_id}/avaliacoes", tags=["avaliacao"])


def _obter_cardapio_ou_404(cardapio_id: int, db: Session) -> Cardapio:
    cardapio = db.get(Cardapio, cardapio_id)
    if cardapio is None:
        raise HTTPException(status_code=404, detail="Cardápio não encontrado")
    return cardapio


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
    identidade: Annotated[UUID, Depends(obter_identidade)],
    db: Session = Depends(get_db),
    instante: datetime = Depends(agora),
):
    cardapio = _obter_cardapio_ou_404(cardapio_id, db)
    exigir_janela_aberta(cardapio, instante)
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
