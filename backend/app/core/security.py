from secrets import compare_digest

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import SecretStr

from app.core.config import settings

bearer = HTTPBearer(auto_error=False)


def _exigir_token(
    credenciais: HTTPAuthorizationCredentials | None, esperado: SecretStr, detalhe: str
) -> None:
    """Recusa quando o segredo não foi configurado (falha fechada) ou o token não confere."""
    segredo = esperado.get_secret_value()
    if (
        not segredo.strip()
        or credenciais is None
        or not compare_digest(credenciais.credentials.encode("utf-8"), segredo.encode("utf-8"))
    ):
        raise HTTPException(
            status_code=401,
            detail=detalhe,
            headers={"WWW-Authenticate": "Bearer"},
        )


def exigir_token_importacao(
    credenciais: HTTPAuthorizationCredentials | None = Depends(bearer),
) -> None:
    """Recusa a escrita administrativa inclusive quando o segredo não foi configurado."""
    _exigir_token(
        credenciais, settings.importacao_token, "Credencial de importação ausente ou inválida"
    )


def exigir_token_equipe(
    credenciais: HTTPAuthorizationCredentials | None = Depends(bearer),
) -> None:
    """Leitura interna das reclamações: exige o token da equipe (D06)."""
    _exigir_token(credenciais, settings.equipe_token, "Credencial da equipe ausente ou inválida")
