from secrets import compare_digest

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import settings

bearer = HTTPBearer(auto_error=False)


def exigir_token_importacao(
    credenciais: HTTPAuthorizationCredentials | None = Depends(bearer),
) -> None:
    """Recusa a escrita administrativa inclusive quando o segredo não foi configurado."""
    esperado = settings.importacao_token.get_secret_value()
    if (
        not esperado.strip()
        or credenciais is None
        or not compare_digest(
            credenciais.credentials.encode("utf-8"), esperado.encode("utf-8")
        )
    ):
        raise HTTPException(
            status_code=401,
            detail="Credencial de importação ausente ou inválida",
            headers={"WWW-Authenticate": "Bearer"},
        )
