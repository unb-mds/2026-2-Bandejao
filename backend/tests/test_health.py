from fastapi.testclient import TestClient

from app.api.routes.health import obter_versao
from app.core.config import Settings
from app.main import app

client = TestClient(app)


def test_health_check_returns_ok():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_raiz_redireciona_para_documentacao():
    response = client.get("/", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/docs"


def test_version_expoe_commit_da_hospedagem(monkeypatch):
    monkeypatch.delenv("APP_VERSION", raising=False)
    monkeypatch.setenv("RENDER_GIT_COMMIT", "abc123def456")

    response = client.get("/version")

    assert response.status_code == 200
    assert response.json() == {"version": "abc123def456"}


def test_version_prioriza_identificador_declarado(monkeypatch):
    monkeypatch.setenv("APP_VERSION", "v2.0.0")
    monkeypatch.setenv("RENDER_GIT_COMMIT", "abc123def456")

    assert obter_versao() == "v2.0.0"


def test_version_local_tem_identificador_padrao(monkeypatch):
    monkeypatch.delenv("APP_VERSION", raising=False)
    monkeypatch.delenv("RENDER_GIT_COMMIT", raising=False)

    assert obter_versao() == "development"


def test_cors_inclui_frontend_publico_sem_barra_final():
    configuracao = Settings(
        _env_file=None,
        cors_origins=["http://localhost:5173"],
        frontend_url="https://bandejao-unb-g12.onrender.com/",
    )

    assert configuracao.origens_cors == [
        "http://localhost:5173",
        "https://bandejao-unb-g12.onrender.com",
    ]


def test_cors_sem_frontend_publico_mantem_origens_configuradas():
    configuracao = Settings(_env_file=None, cors_origins=["http://localhost:5173"])

    assert configuracao.origens_cors == ["http://localhost:5173"]


def test_url_do_render_seleciona_driver_psycopg():
    configuracao = Settings(
        _env_file=None,
        database_url="postgresql://usuario:senha@banco/bandejao",
    )
    url_legada = Settings(
        _env_file=None,
        database_url="postgres://usuario:senha@banco/bandejao",
    )

    assert (
        configuracao.database_url_sqlalchemy
        == "postgresql+psycopg://usuario:senha@banco/bandejao"
    )
    assert (
        url_legada.database_url_sqlalchemy
        == "postgresql+psycopg://usuario:senha@banco/bandejao"
    )


def test_url_que_ja_declara_driver_permanece_inalterada():
    configuracao = Settings(
        _env_file=None,
        database_url="postgresql+psycopg://usuario:senha@banco/bandejao",
    )

    assert (
        configuracao.database_url_sqlalchemy
        == "postgresql+psycopg://usuario:senha@banco/bandejao"
    )
