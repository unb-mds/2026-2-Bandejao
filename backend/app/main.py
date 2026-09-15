from fastapi import FastAPI

from app.api.routes import avaliacao, campus, cardapio, checkin, health
from app.core.config import settings

app = FastAPI(title=settings.app_name)

app.include_router(health.router)
app.include_router(campus.router)
app.include_router(cardapio.router)
app.include_router(avaliacao.router)
app.include_router(checkin.router)