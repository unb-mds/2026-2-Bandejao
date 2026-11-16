from collections.abc import Callable, Generator
from datetime import datetime
import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.tempo import FUSO_BRASILIA, agora
from app.db.session import Base, get_db
from app.main import app


def criar_engine_teste(database_url: str | None = None):
    """Usa PostgreSQL quando configurado e SQLite isolado no desenvolvimento local."""
    url = database_url or os.getenv("TEST_DATABASE_URL")
    if url:
        return create_engine(url)
    return create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )


@pytest.fixture()
def db_session() -> Generator[Session, None, None]:
    engine = criar_engine_teste()
    testing_session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    session = testing_session_local()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


@pytest.fixture()
def client(db_session: Session) -> Generator[TestClient, None, None]:
    # Faz as rotas usarem o banco isolado do teste, sem tocar no PostgreSQL configurado.
    def override_get_db() -> Generator[Session, None, None]:
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture()
def definir_agora() -> Generator[Callable[..., datetime], None, None]:
    """Fixa o relógio da API em um instante de America/Sao_Paulo."""

    def _definir(ano, mes, dia, hora=0, minuto=0, segundo=0) -> datetime:
        instante = datetime(ano, mes, dia, hora, minuto, segundo, tzinfo=FUSO_BRASILIA)
        app.dependency_overrides[agora] = lambda: instante
        return instante

    yield _definir
    app.dependency_overrides.pop(agora, None)
