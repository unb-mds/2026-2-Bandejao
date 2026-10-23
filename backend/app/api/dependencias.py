"""Dependências compartilhadas por avaliações e reclamações (D03, D04, RN05)."""

from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi import Header, HTTPException

from app.core.tempo import FUSO_BRASILIA, avaliacao_esta_aberta
from app.models.cardapio import Cardapio


def obter_identidade(
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


def exigir_janela_aberta(cardapio: Cardapio, instante: datetime) -> None:
    """RF04/RF08/RN05: só aceita do início do serviço até antes das 00h do dia seguinte."""
    if avaliacao_esta_aberta(cardapio.tipo_refeicao, cardapio.data, instante):
        return
    if instante.astimezone(FUSO_BRASILIA).date() > cardapio.data:
        detalhe = "O prazo terminou às 00h do dia seguinte à refeição"
    else:
        detalhe = "O envio só é aceito a partir do início do serviço da refeição"
    raise HTTPException(status_code=422, detail=detalhe)
