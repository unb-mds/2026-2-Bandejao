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
    equipe_token: SecretStr = SecretStr("")
    database_url: str = "postgresql+psycopg://bandejao:bandejao@localhost:5432/bandejao"
    cors_origins: list[str] = Field(
        default_factory=lambda: ["http://localhost:5173", "http://127.0.0.1:5173"]
    )
    frontend_url: str = ""

    @property
    def origens_cors(self) -> list[str]:
        """Combina as origens locais com a URL pública informada pelo ambiente."""
        origem_publica = self.frontend_url.rstrip("/")
        return [*self.cors_origins, origem_publica] if origem_publica else self.cors_origins

    @property
    def database_url_sqlalchemy(self) -> str:
        """Seleciona explicitamente o driver psycopg para URLs fornecidas pela hospedagem."""
        if self.database_url.startswith("postgresql://"):
            return self.database_url.replace("postgresql://", "postgresql+psycopg://", 1)
        if self.database_url.startswith("postgres://"):
            return self.database_url.replace("postgres://", "postgresql+psycopg://", 1)
        return self.database_url


settings = Settings()
