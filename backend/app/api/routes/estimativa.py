"""RF07/D05: estimativas por refeição, com dados reais e simulados separados."""

from datetime import date, datetime

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from app.core import config
from app.core.tempo import agora
from app.db.session import get_db
from app.models import Campus, Cardapio, Intencao, TipoRefeicao
from app.schemas.estimativa import EstimativaRead

router = APIRouter(prefix="/estimativas", tags=["estimativa"])


@router.get("/", response_model=list[EstimativaRead], response_model_exclude_none=True)
def listar_estimativas(
    response: Response,
    campus_id: int = Query(gt=0),
    data_inicio: date = Query(),
    data_fim: date = Query(),
    tipo_refeicao: TipoRefeicao | None = Query(default=None),
    dados_simulados: bool = Query(
        default=False,
        description="Consulta somente dados simulados quando true; nunca soma aos reais.",
    ),
    db: Session = Depends(get_db),
    instante: datetime = Depends(agora),
) -> list[EstimativaRead]:
    response.headers["Cache-Control"] = "no-store"
    if data_inicio > data_fim:
        raise HTTPException(status_code=422, detail="data_inicio deve ser menor ou igual a data_fim")
    if db.get(Campus, campus_id) is None:
        raise HTTPException(status_code=404, detail="Campus não encontrado")

    # O LEFT JOIN mantém refeições que ainda não receberam nenhuma intenção.
    consulta = (
        db.query(Cardapio, func.count(Intencao.id))
        .outerjoin(Intencao, and_(
            Intencao.cardapio_id == Cardapio.id,
            Intencao.ativa.is_(True),
            Intencao.simulada.is_(dados_simulados),
        ))
        .filter(
            Cardapio.campus_id == campus_id,
            Cardapio.data >= data_inicio,
            Cardapio.data <= data_fim,
        )
    )
    if tipo_refeicao is not None:
        consulta = consulta.filter(Cardapio.tipo_refeicao == tipo_refeicao)

    resultado = []
    for cardapio, total in consulta.group_by(Cardapio.id).order_by(
        Cardapio.data, Cardapio.tipo_refeicao, Cardapio.id,
    ).all():
        suficiente = total >= config.AMOSTRA_MINIMA_ESTIMATIVA
        resultado.append(EstimativaRead(
            cardapio_id=cardapio.id,
            campus_id=cardapio.campus_id,
            data=cardapio.data,
            tipo_refeicao=cardapio.tipo_refeicao,
            data_inicio=data_inicio,
            data_fim=data_fim,
            calculado_em=instante,
            dados_simulados=dados_simulados,
            amostra_minima=config.AMOSTRA_MINIMA_ESTIMATIVA,
            status="disponivel" if suficiente else "dados_insuficientes",
            mensagem=(
                "Estimativa de intenções; não representa a fila real."
                if suficiente else
                "Dados insuficientes para estimar intenções; não representa a fila real."
            ),
            contagem=total if suficiente else None,
        ))
    return resultado
