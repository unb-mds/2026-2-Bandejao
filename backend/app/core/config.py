from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    app_name: str = "Bandejão API"
    database_url: str = "postgresql+psycopg://bandejao:bandejao@localhost:5432/bandejao"


settings = Settings()
