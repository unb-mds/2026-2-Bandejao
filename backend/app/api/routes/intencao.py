"""RF06: marcação antes do serviço e consulta de intenções reais da identidade."""

from datetime import date, datetime
import re
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.dependencias import obter_identidade
from app.core.config import HORARIOS_INICIO_REFEICAO
from app.core.tempo import FUSO_BRASILIA, agora, limites_da_semana
from app.db.session import get_db
from app.models import Cardapio, Intencao
from app.schemas.intencao import IntencaoPessoalRead, IntencaoRead

router = APIRouter(tags=["intencao"])
CAMINHO = "/cardapios/{cardapio_id}/intencao/"


def _obter_cardapio(cardapio_id: int, db: Session) -> Cardapio:
    cardapio = db.get(Cardapio, cardapio_id)
    if cardapio is None:
        raise HTTPException(status_code=404, detail="Cardápio não encontrado")
    return cardapio


def _obter_intencao(cardapio_id: int, identidade: UUID, db: Session) -> Intencao | None:
    return db.query(Intencao).filter_by(cardapio_id=cardapio_id, identidade=identidade).one_or_none()


def _exigir_prazo(cardapio: Cardapio, instante: datetime) -> None:
    horario = HORARIOS_INICIO_REFEICAO.get(cardapio.tipo_refeicao.value)
    if horario is None:
        raise HTTPException(status_code=422, detail="Horário de início do serviço não configurado")
    inicio = datetime.combine(cardapio.data, horario, tzinfo=FUSO_BRASILIA)
    if instante.astimezone(FUSO_BRASILIA) >= inicio:
        raise HTTPException(
            status_code=422,
            detail="A intenção só pode ser marcada antes do início do serviço da refeição",
        )


def _ativar(intencao: Intencao) -> None:
    # Um UUID reservado para demonstração nunca se transforma em intenção real pela API.
    if intencao.simulada:
        raise HTTPException(status_code=409, detail="Identidade indisponível para esta refeição")
    intencao.ativa = True


@router.put(CAMINHO, response_model=IntencaoRead)
def marcar_intencao(
    cardapio_id: int,
    identidade: Annotated[UUID, Depends(obter_identidade)],
    db: Session = Depends(get_db),
    instante: datetime = Depends(agora),
):
    cardapio = _obter_cardapio(cardapio_id, db)
    _exigir_prazo(cardapio, instante)
    intencao = _obter_intencao(cardapio_id, identidade, db)
    if intencao is not None:
        _ativar(intencao)
        db.commit()
    else:
        db.add(Intencao(cardapio_id=cardapio_id, identidade=identidade))
        try:
            db.commit()
        except IntegrityError:
            # Outra requisição pode ter inserido a mesma chave entre a leitura e o commit.
            db.rollback()
            concorrente = _obter_intencao(cardapio_id, identidade, db)
            if concorrente is None:
                raise
            _ativar(concorrente)
            db.commit()
    return IntencaoRead(cardapio_id=cardapio_id, ativa=True)


@router.get(CAMINHO, response_model=IntencaoRead)
def obter_intencao(
    cardapio_id: int,
    response: Response,
    identidade: Annotated[UUID, Depends(obter_identidade)],
    db: Session = Depends(get_db),
):
    _obter_cardapio(cardapio_id, db)
    response.headers["Cache-Control"] = "no-store"
    intencao = _obter_intencao(cardapio_id, identidade, db)
    return IntencaoRead(
        cardapio_id=cardapio_id,
        ativa=bool(intencao and not intencao.simulada and intencao.ativa),
    )


@router.delete(CAMINHO, response_model=IntencaoRead)
def desmarcar_intencao(
    cardapio_id: int,
    identidade: Annotated[UUID, Depends(obter_identidade)],
    db: Session = Depends(get_db),
):
    _obter_cardapio(cardapio_id, db)
    intencao = _obter_intencao(cardapio_id, identidade, db)
    # RF06 limita o prazo para marcar. Cancelar continua removendo a contribuição após o início.
    if intencao is not None and not intencao.simulada:
        intencao.ativa = False
        db.commit()
    return IntencaoRead(cardapio_id=cardapio_id, ativa=False)


def _validar_data(valor: str) -> date:
    try:
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", valor):
            raise ValueError
        return date.fromisoformat(valor)
    except ValueError:
        raise HTTPException(status_code=422, detail="Use datas válidas no formato YYYY-MM-DD") from None


@router.get("/intencoes/", response_model=list[IntencaoPessoalRead])
def listar_intencoes(
    response: Response,
    identidade: Annotated[UUID, Depends(obter_identidade)],
    campus_id: int | None = Query(default=None, gt=0),
    data_inicio: str | None = Query(default=None),
    data_fim: str | None = Query(default=None),
    db: Session = Depends(get_db),
    instante: datetime = Depends(agora),
):
    response.headers["Cache-Control"] = "no-store"
    if data_inicio is None and data_fim is None:
        inicio, fim = limites_da_semana(instante)
    elif data_inicio is None or data_fim is None:
        raise HTTPException(status_code=422, detail="Informe data_inicio e data_fim juntas")
    else:
        inicio, fim = _validar_data(data_inicio), _validar_data(data_fim)
        if inicio > fim:
            raise HTTPException(status_code=422, detail="data_inicio deve ser menor ou igual a data_fim")
    consulta = db.query(Cardapio).join(Intencao).filter(
        Intencao.identidade == identidade,
        Intencao.ativa.is_(True),
        Intencao.simulada.is_(False),
        Cardapio.data >= inicio,
        Cardapio.data <= fim,
    )
    if campus_id is not None:
        consulta = consulta.filter(Cardapio.campus_id == campus_id)
    return [
        IntencaoPessoalRead(
            cardapio_id=cardapio.id, campus_id=cardapio.campus_id, data=cardapio.data,
            tipo_refeicao=cardapio.tipo_refeicao, ativa=True,
        )
        for cardapio in consulta.order_by(
            Cardapio.data, Cardapio.campus_id, Cardapio.tipo_refeicao, Cardapio.id
        ).all()
    ]
