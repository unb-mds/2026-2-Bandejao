from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from app.api.routes import avaliacao, campus, cardapio, checkin, health
from app.core.config import settings

app = FastAPI(title=settings.app_name)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/", include_in_schema=False)
def abrir_documentacao() -> RedirectResponse:
    """Direciona a URL base para a prévia interativa da API."""
    return RedirectResponse(url="/docs")


app.include_router(health.router)
app.include_router(campus.router)
app.include_router(cardapio.router)
app.include_router(avaliacao.router)
app.include_router(checkin.router)
