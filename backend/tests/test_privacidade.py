"""A identidade usada nas rotas nunca deve aparecer em respostas da API."""

from datetime import date
from uuid import UUID, uuid4

from fastapi.testclient import TestClient
from pydantic import SecretStr
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models import Intencao
from tests.test_cardapio_api import criar_cardapio_de_teste

IDENTIDADE_PRIVADA = "123e4567-e89b-42d3-a456-426614174099"


def _assert_identidade_ausente(response, identidade: str = IDENTIDADE_PRIVADA) -> None:
    assert identidade not in response.text
    if response.status_code < 400:
        body = response.json()
        registros = body if isinstance(body, list) else [body]
        assert all("identidade" not in registro for registro in registros)


def test_avaliacao_nao_revela_identidade_em_respostas_de_sucesso_ou_erro(
    client: TestClient, db_session: Session, definir_agora
):
    cardapio = criar_cardapio_de_teste(db_session)
    url = f"/cardapios/{cardapio.id}/avaliacoes/"
    headers = {"X-Identidade": IDENTIDADE_PRIVADA}

    definir_agora(2026, 9, 15, 12)
    criada = client.post(url, headers=headers, json={"nota": 5})
    assert criada.status_code == 201
    _assert_identidade_ausente(criada)

    listada = client.get(url)
    assert listada.status_code == 200
    _assert_identidade_ausente(listada)

    definir_agora(2026, 9, 16, 0)
    recusada = client.post(url, headers=headers, json={"nota": 4})
    assert recusada.status_code == 422
    _assert_identidade_ausente(recusada)


def test_reclamacao_nao_revela_identidade_em_sucesso_erro_ou_leitura_interna(
    client: TestClient, db_session: Session, definir_agora, monkeypatch
):
    cardapio = criar_cardapio_de_teste(db_session)
    url = f"/cardapios/{cardapio.id}/reclamacoes/"
    headers = {"X-Identidade": IDENTIDADE_PRIVADA}
    definir_agora(2026, 9, 15, 12)

    criada = client.post(
        url, headers=headers, json={"categoria": "higiene", "descricao": "Mesa suja."}
    )
    assert criada.status_code == 201
    assert set(criada.json()) == {"id", "mensagem"}
    _assert_identidade_ausente(criada)

    recusada = client.post(
        url, headers=headers, json={"categoria": "desconhecida", "descricao": "Mesa suja."}
    )
    assert recusada.status_code == 422
    _assert_identidade_ausente(recusada)

    token = "token-interno-privacidade"
    monkeypatch.setattr(settings, "equipe_token", SecretStr(token))
    interna = client.get("/equipe/reclamacoes/", headers={"Authorization": f"Bearer {token}"})
    assert interna.status_code == 200
    assert set(interna.json()[0]) == {"id", "cardapio_id", "categoria", "descricao", "criado_em"}
    _assert_identidade_ausente(interna)


def test_intencao_nao_revela_identidade_em_sucesso_ou_erro(
    client: TestClient, db_session: Session, definir_agora
):
    cardapio = criar_cardapio_de_teste(db_session)
    url = f"/cardapios/{cardapio.id}/intencao/"
    headers = {"X-Identidade": IDENTIDADE_PRIVADA}

    definir_agora(2026, 9, 15, 10, 59)
    marcada = client.put(url, headers=headers)
    assert marcada.status_code == 200
    _assert_identidade_ausente(marcada)

    pessoal = client.get("/intencoes/", headers=headers)
    assert pessoal.status_code == 200
    _assert_identidade_ausente(pessoal)

    definir_agora(2026, 9, 15, 11)
    recusada = client.put(url, headers=headers)
    assert recusada.status_code == 422
    _assert_identidade_ausente(recusada)


def test_estimativa_nao_revela_identidades_em_sucesso_ou_erro(
    client: TestClient, db_session: Session, definir_agora
):
    cardapio = criar_cardapio_de_teste(db_session)
    definir_agora(2026, 9, 15, 10)
    identidades = [UUID(IDENTIDADE_PRIVADA), *(uuid4() for _ in range(9))]
    db_session.add_all(
        Intencao(cardapio_id=cardapio.id, identidade=identidade) for identidade in identidades
    )
    db_session.commit()
    params = {
        "campus_id": cardapio.campus_id,
        "data_inicio": date(2026, 9, 15).isoformat(),
        "data_fim": date(2026, 9, 15).isoformat(),
    }
    headers = {"X-Identidade": IDENTIDADE_PRIVADA}

    estimativa = client.get("/estimativas/", params=params, headers=headers)
    assert estimativa.status_code == 200
    _assert_identidade_ausente(estimativa)
    assert estimativa.json()[0]["contagem"] == 10

    params["data_inicio"] = "2026-09-16"
    recusada = client.get("/estimativas/", params=params, headers=headers)
    assert recusada.status_code == 422
    _assert_identidade_ausente(recusada)
