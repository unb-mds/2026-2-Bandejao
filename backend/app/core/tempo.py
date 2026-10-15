"""Convenções de data e semana adotadas pelo Bandejão."""

from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo


FUSO_BRASILIA = ZoneInfo("America/Sao_Paulo")


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
