from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.dependencias import exigir_janela_aberta, obter_identidade
from app.core.security import exigir_token_equipe
from app.core.tempo import agora
from app.db.session import get_db
from app.models.cardapio import Cardapio
from app.models.enums import CategoriaReclamacao
from app.models.reclamacao import Reclamacao
from app.schemas.reclamacao import ReclamacaoConfirmacao, ReclamacaoCreate, ReclamacaoEquipeRead

# Registro: só o POST existe. Não há listagem pública (CA-RF08-04).
router = APIRouter(prefix="/cardapios/{cardapio_id}/reclamacoes", tags=["reclamacao"])

# Leitura interna, protegida por token da equipe.
router_equipe = APIRouter(
    prefix="/equipe/reclamacoes",
    tags=["reclamacao"],
    dependencies=[Depends(exigir_token_equipe)],
)


@router.post("/", response_model=ReclamacaoConfirmacao, status_code=201)
def registrar_reclamacao(
    cardapio_id: int,
    payload: ReclamacaoCreate,
    identidade: Annotated[UUID, Depends(obter_identidade)],
    db: Session = Depends(get_db),
    instante: datetime = Depends(agora),
) -> ReclamacaoConfirmacao:
    cardapio = db.get(Cardapio, cardapio_id)
    if cardapio is None:
        raise HTTPException(status_code=404, detail="Cardápio não encontrado")
    exigir_janela_aberta(cardapio, instante)

    reclamacao = Reclamacao(
        cardapio_id=cardapio_id,
        identidade=identidade,
        categoria=payload.categoria,
        descricao=payload.descricao,
        criado_em=instante,
    )
    db.add(reclamacao)
    db.commit()
    return ReclamacaoConfirmacao(id=reclamacao.id)


@router_equipe.get("/", response_model=list[ReclamacaoEquipeRead])
def listar_reclamacoes_da_equipe(
    cardapio_id: int | None = Query(default=None),
    categoria: CategoriaReclamacao | None = Query(default=None),
    db: Session = Depends(get_db),
) -> list[Reclamacao]:
    query = db.query(Reclamacao)
    if cardapio_id is not None:
        query = query.filter(Reclamacao.cardapio_id == cardapio_id)
    if categoria is not None:
        query = query.filter(Reclamacao.categoria == categoria)
    return query.order_by(Reclamacao.criado_em.desc(), Reclamacao.id.desc()).all()
