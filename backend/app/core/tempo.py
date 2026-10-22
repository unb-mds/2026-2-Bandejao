"""Convenções temporais e janelas de serviço adotadas pelo Bandejão."""

from datetime import date, datetime, time, timedelta
from typing import Mapping
from zoneinfo import ZoneInfo

from app.core.config import HORARIOS_INICIO_REFEICAO
from app.models.enums import TipoRefeicao


FUSO_BRASILIA = ZoneInfo("America/Sao_Paulo")


def agora() -> datetime:
    """Relógio da aplicação em Brasília; as rotas o recebem por Depends para os testes o fixarem."""
    return datetime.now(FUSO_BRASILIA)


def data_em_brasilia(instante: datetime) -> date:
    """Converte um instante com fuso para a data civil de Brasília."""
    if instante.tzinfo is None or instante.utcoffset() is None:
        raise ValueError("O instante deve informar o fuso horário")
    return instante.astimezone(FUSO_BRASILIA).date()


def limites_da_semana(referencia: date | datetime) -> tuple[date, date]:
    """Devolve a segunda e o domingo da semana da referência em Brasília."""
    if isinstance(referencia, datetime):
        data_referencia = data_em_brasilia(referencia)
    elif isinstance(referencia, date):
        data_referencia = referencia
    else:
        raise TypeError("A referência deve ser uma data ou um instante com fuso")

    inicio = data_referencia - timedelta(days=data_referencia.weekday())
    fim = inicio + timedelta(days=6)
    return inicio, fim


def avaliacao_esta_aberta(
    tipo_refeicao: TipoRefeicao,
    data_refeicao: date,
    instante: datetime,
    *,
    horarios_inicio: Mapping[str, time] = HORARIOS_INICIO_REFEICAO,
) -> bool:
    """Informa se uma refeição existente está na janela de avaliação."""
    if instante.tzinfo is None or instante.utcoffset() is None:
        raise ValueError("O instante deve informar o fuso horário")

    horario_inicio = horarios_inicio.get(tipo_refeicao.value)
    if horario_inicio is None:
        return False

    instante_brasilia = instante.astimezone(FUSO_BRASILIA)
    inicio = datetime.combine(data_refeicao, horario_inicio, tzinfo=FUSO_BRASILIA)
    fim = datetime.combine(data_refeicao + timedelta(days=1), time.min, tzinfo=FUSO_BRASILIA)
    return inicio <= instante_brasilia < fim
