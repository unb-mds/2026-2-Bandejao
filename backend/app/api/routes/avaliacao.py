from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.avaliacao import Avaliacao
from app.models.cardapio import Cardapio
from app.schemas.avaliacao import AvaliacaoCreate, AvaliacaoRead

router = APIRouter(prefix="/cardapios/{cardapio_id}/avaliacoes", tags=["avaliacao"])


def _obter_cardapio_ou_404(cardapio_id: int, db: Session) -> None:
    if db.get(Cardapio, cardapio_id) is None:
        raise HTTPException(status_code=404, detail="Cardápio não encontrado")


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
    cardapio_id: int, payload: AvaliacaoCreate, db: Session = Depends(get_db)
):
    _obter_cardapio_ou_404(cardapio_id, db)
    avaliacao = Avaliacao(cardapio_id=cardapio_id, **payload.model_dump())
    db.add(avaliacao)
    db.commit()
    db.refresh(avaliacao)
    return avaliacao
