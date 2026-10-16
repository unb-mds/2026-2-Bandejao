from datetime import time
from types import MappingProxyType
from typing import Mapping

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

AMOSTRA_MINIMA_ESTIMATIVA = 10
# Fonte consultada em 15/10/2026: https://ru.unb.br/
HORARIOS_INICIO_REFEICAO: Mapping[str, time] = MappingProxyType(
    {
        "cafe_da_manha": time(7, 0),
        "almoco": time(11, 0),
        "jantar": time(17, 0),
    }
)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    app_name: str = "Bandejão API"
    importacao_token: SecretStr = SecretStr("")
    database_url: str = "postgresql+psycopg://bandejao:bandejao@localhost:5432/bandejao"
    cors_origins: list[str] = Field(
        default_factory=lambda: ["http://localhost:5173", "http://127.0.0.1:5173"]
    )


settings = Settings()
