import os

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


def obter_versao() -> str:
    """Retorna a versão declarada ou o commit informado pela hospedagem."""
    return os.getenv("APP_VERSION") or os.getenv("RENDER_GIT_COMMIT") or "development"


@router.get("/version")
def version_check() -> dict[str, str]:
    return {"version": obter_versao()}
