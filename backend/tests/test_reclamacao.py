"""RF08 / CA-RF08-01 a 04 / RN07 / RN10 / D06 — registro e leitura interna de reclamações."""

from datetime import date

import pytest
from fastapi.testclient import TestClient
from pydantic import SecretStr
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.tempo import FUSO_BRASILIA
from app.models import Avaliacao, Cardapio, ItemCardapio, Reclamacao
from tests.test_cardapio_api import IDENTIDADE_1, IDENTIDADE_2, criar_cardapio_de_teste

TOKEN_EQUIPE = "token-equipe-apenas-para-teste"
TOKEN_IMPORTACAO = "segredo-apenas-para-teste"


@pytest.fixture()
def equipe_headers(monkeypatch):
    monkeypatch.setattr(settings, "equipe_token", SecretStr(TOKEN_EQUIPE))
    return {"Authorization": f"Bearer {TOKEN_EQUIPE}"}


def _reclamar(client: TestClient, cardapio_id: int, identidade: str = IDENTIDADE_1, **corpo):
    corpo = {"categoria": "qualidade", "descricao": "Arroz frio.", **corpo}
    return client.post(
        f"/cardapios/{cardapio_id}/reclamacoes/",
        headers={"X-Identidade": identidade},
        json=corpo,
    )


@pytest.fixture()
def cardapio(db_session: Session, definir_agora):
    """Almoço de 15/09/2026 com o relógio às 12h, dentro da janela."""
    definir_agora(2026, 9, 15, 12)
    return criar_cardapio_de_teste(db_session)


# --- CA-RF08-01: registro válido ---------------------------------------------------------


@pytest.mark.parametrize("categoria", ["qualidade", "higiene", "atendimento", "outros"])
def test_registra_reclamacao_em_cada_categoria_sem_exigir_nota(
    client: TestClient, db_session: Session, cardapio: Cardapio, categoria: str
):
    response = _reclamar(client, cardapio.id, categoria=categoria)

    assert response.status_code == 201
    reclamacao = db_session.query(Reclamacao).one()
    assert response.json()["id"] == reclamacao.id
    assert reclamacao.cardapio_id == cardapio.id
    assert reclamacao.categoria.value == categoria
    assert str(reclamacao.identidade) == IDENTIDADE_1
    assert db_session.query(Avaliacao).count() == 0


def test_grava_o_instante_do_envio_e_remove_espacos_das_pontas(
    client: TestClient, db_session: Session, cardapio: Cardapio, definir_agora
):
    instante = definir_agora(2026, 9, 15, 13, 45, 10)

    response = _reclamar(client, cardapio.id, descricao="  Faltou talher.\n ")

    assert response.status_code == 201
    reclamacao = db_session.query(Reclamacao).one()
    assert reclamacao.descricao == "Faltou talher."
    # O SQLite devolve o instante sem fuso; o valor gravado é o relógio de Brasília.
    assert reclamacao.criado_em.replace(tzinfo=FUSO_BRASILIA) == instante


@pytest.mark.parametrize("tamanho", [1, 1000])
def test_aceita_os_limites_da_descricao(
    client: TestClient, db_session: Session, cardapio: Cardapio, tamanho: int
):
    assert _reclamar(client, cardapio.id, descricao="a" * tamanho).status_code == 201
    assert db_session.query(Reclamacao).one().descricao == "a" * tamanho


def test_varias_reclamacoes_da_mesma_identidade_sao_aceitas(
    client: TestClient, db_session: Session, cardapio: Cardapio
):
    assert _reclamar(client, cardapio.id, descricao="Primeira.").status_code == 201
    assert _reclamar(client, cardapio.id, descricao="Segunda.").status_code == 201
    assert db_session.query(Reclamacao).count() == 2


# --- CA-RF08-02: recusas sem gravar ------------------------------------------------------


@pytest.mark.parametrize(
    ("corpo", "campo"),
    [
        ({"categoria": "quantidade"}, "categoria"),
        ({"categoria": "Qualidade da comida"}, "categoria"),
        ({"descricao": ""}, "descricao"),
        ({"descricao": "   \n "}, "descricao"),
        ({"descricao": "a" * 1001}, "descricao"),
        ({"descricao": f"  {'a' * 1001}  "}, "descricao"),
    ],
)
def test_recusa_categoria_ou_descricao_invalida_com_o_motivo(
    client: TestClient, db_session: Session, cardapio: Cardapio, corpo: dict, campo: str
):
    response = _reclamar(client, cardapio.id, **corpo)

    assert response.status_code == 422
    assert campo in response.json()["detail"][0]["loc"]
    assert db_session.query(Reclamacao).count() == 0


def test_recusa_corpo_sem_categoria_ou_sem_descricao(
    client: TestClient, db_session: Session, cardapio: Cardapio
):
    url = f"/cardapios/{cardapio.id}/reclamacoes/"
    headers = {"X-Identidade": IDENTIDADE_1}

    assert client.post(url, headers=headers, json={"descricao": "x"}).status_code == 422
    assert client.post(url, headers=headers, json={"categoria": "higiene"}).status_code == 422
    assert db_session.query(Reclamacao).count() == 0


def test_recusa_refeicao_inexistente(client: TestClient, db_session: Session, definir_agora):
    definir_agora(2026, 9, 15, 12)

    response = _reclamar(client, 999)

    assert response.status_code == 404
    assert response.json()["detail"] == "Cardápio não encontrado"
    assert db_session.query(Reclamacao).count() == 0


@pytest.mark.parametrize("identidade", [None, "nao-e-uuid", "6ba7b810-9dad-11d1-80b4-00c04fd430c8"])
def test_recusa_identidade_ausente_ou_fora_da_versao_4(
    client: TestClient, db_session: Session, cardapio: Cardapio, identidade
):
    headers = {} if identidade is None else {"X-Identidade": identidade}

    response = client.post(
        f"/cardapios/{cardapio.id}/reclamacoes/",
        headers=headers,
        json={"categoria": "outros", "descricao": "x"},
    )

    assert response.status_code == 400
    assert "UUID v4" in response.json()["detail"]
    assert db_session.query(Reclamacao).count() == 0


def test_recusa_fora_da_janela_da_refeicao_com_o_motivo(
    client: TestClient, db_session: Session, definir_agora
):
    cardapio = criar_cardapio_de_teste(db_session)

    definir_agora(2026, 9, 15, 10, 59, 59)
    antes = _reclamar(client, cardapio.id)
    definir_agora(2026, 9, 16, 0, 0, 0)
    depois = _reclamar(client, cardapio.id)

    assert antes.status_code == 422
    assert "início do serviço" in antes.json()["detail"]
    assert depois.status_code == 422
    assert "00h do dia seguinte" in depois.json()["detail"]
    assert db_session.query(Reclamacao).count() == 0


# --- CA-RF08-03: a confirmação não promete nada ------------------------------------------


def test_confirmacao_nao_promete_encaminhamento_nem_publicacao(
    client: TestClient, cardapio: Cardapio
):
    corpo = _reclamar(client, cardapio.id).json()

    assert set(corpo) == {"id", "mensagem"}
    assert corpo["mensagem"] == "Reclamação registrada."
    texto = corpo["mensagem"].lower()
    for palavra in ["encaminh", "enviad", "ru ", "resposta", "public", "divulg"]:
        assert palavra not in texto


# --- CA-RF08-04: nenhuma rota pública de leitura -----------------------------------------


def test_nao_existe_rota_publica_de_listagem_nem_de_leitura(
    client: TestClient, cardapio: Cardapio
):
    _reclamar(client, cardapio.id, descricao="Texto sigiloso.")
    caminhos = [
        f"/cardapios/{cardapio.id}/reclamacoes/",
        f"/cardapios/{cardapio.id}/reclamacoes/1",
        "/reclamacoes/",
    ]

    for identidade in (IDENTIDADE_1, IDENTIDADE_2):
        for caminho in caminhos:
            response = client.get(caminho, headers={"X-Identidade": identidade})
            assert response.status_code in (404, 405)
            assert "Texto sigiloso." not in response.text

    nomes = {rota.path for rota in client.app.routes}
    assert "/cardapios/{cardapio_id}/reclamacoes/" in nomes
    publicas_com_get = [
        rota.path
        for rota in client.app.routes
        if "reclamacoes" in rota.path
        and "GET" in getattr(rota, "methods", set())
        and not rota.path.startswith("/equipe/")
    ]
    assert publicas_com_get == []


def test_outras_rotas_publicas_nao_expoem_reclamacoes(client: TestClient, cardapio: Cardapio):
    _reclamar(client, cardapio.id, descricao="Texto sigiloso.")

    for caminho in [
        f"/cardapios/{cardapio.id}",
        "/cardapios/",
        f"/cardapios/{cardapio.id}/avaliacoes/",
    ]:
        assert "Texto sigiloso." not in client.get(caminho).text


# --- CA-RF08-04: leitura da equipe exige token -------------------------------------------


@pytest.mark.parametrize("authorization", [None, "Bearer incorreto", "Basic incorreto", "Bearer"])
def test_leitura_da_equipe_exige_token_valido(
    client: TestClient, cardapio: Cardapio, equipe_headers, authorization
):
    _reclamar(client, cardapio.id, descricao="Texto sigiloso.")
    headers = {} if authorization is None else {"Authorization": authorization}

    response = client.get("/equipe/reclamacoes/", headers=headers)

    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"
    assert "Texto sigiloso." not in response.text
    assert TOKEN_EQUIPE not in response.text


@pytest.mark.parametrize("token_configurado", ["", "   "])
def test_leitura_da_equipe_sem_segredo_configurado_falha_fechada(
    client: TestClient, cardapio: Cardapio, monkeypatch, token_configurado
):
    monkeypatch.setattr(settings, "equipe_token", SecretStr(token_configurado))
    _reclamar(client, cardapio.id)

    response = client.get(
        "/equipe/reclamacoes/", headers={"Authorization": "Bearer qualquer-token"}
    )

    assert response.status_code == 401


def test_token_de_importacao_nao_abre_a_leitura_da_equipe(
    client: TestClient, cardapio: Cardapio, equipe_headers, monkeypatch
):
    monkeypatch.setattr(settings, "importacao_token", SecretStr(TOKEN_IMPORTACAO))
    _reclamar(client, cardapio.id)

    response = client.get(
        "/equipe/reclamacoes/", headers={"Authorization": f"Bearer {TOKEN_IMPORTACAO}"}
    )

    assert response.status_code == 401


def test_equipe_le_reclamacoes_sem_identidade_e_com_filtros(
    client: TestClient, db_session: Session, cardapio: Cardapio, equipe_headers, definir_agora
):
    definir_agora(2026, 9, 15, 12)
    _reclamar(client, cardapio.id, IDENTIDADE_1, categoria="higiene", descricao="Mesa suja.")
    definir_agora(2026, 9, 15, 14)
    _reclamar(client, cardapio.id, IDENTIDADE_2, categoria="atendimento", descricao="Fila lenta.")

    todas = client.get("/equipe/reclamacoes/", headers=equipe_headers)
    assert todas.status_code == 200
    assert [r["descricao"] for r in todas.json()] == ["Fila lenta.", "Mesa suja."]
    assert all("identidade" not in r for r in todas.json())
    assert set(todas.json()[0]) == {"id", "cardapio_id", "categoria", "descricao", "criado_em"}

    por_categoria = client.get(
        "/equipe/reclamacoes/", params={"categoria": "higiene"}, headers=equipe_headers
    )
    assert [r["descricao"] for r in por_categoria.json()] == ["Mesa suja."]

    outro_cardapio = client.get(
        "/equipe/reclamacoes/", params={"cardapio_id": cardapio.id + 1}, headers=equipe_headers
    )
    assert outro_cardapio.json() == []
    mesmo_cardapio = client.get(
        "/equipe/reclamacoes/", params={"cardapio_id": cardapio.id}, headers=equipe_headers
    )
    assert len(mesmo_cardapio.json()) == 2


# --- RN07: reimportar não apaga ----------------------------------------------------------


def test_reimportar_o_cardapio_nao_apaga_as_reclamacoes(
    client: TestClient, db_session: Session, cardapio: Cardapio, monkeypatch, equipe_headers
):
    monkeypatch.setattr(settings, "importacao_token", SecretStr(TOKEN_IMPORTACAO))
    cardapio_id = cardapio.id
    _reclamar(client, cardapio_id, descricao="Texto preservado.")
    payload = {
        "campus": "Gama",
        "refeicoes": [
            {
                "data": "2026-09-15",
                "tipo_refeicao": "almoco",
                "itens": [
                    {
                        "categoria": "prato_principal",
                        "tipo_dieta": "padrao",
                        "nome": "Lentilha",
                        "alergenos": [],
                    }
                ],
            }
        ],
    }

    resposta = client.post(
        "/cardapios/importacao",
        json=payload,
        headers={"Authorization": f"Bearer {TOKEN_IMPORTACAO}"},
    )

    assert resposta.status_code == 200
    db_session.expire_all()
    assert db_session.query(Cardapio).filter_by(data=date(2026, 9, 15)).one().id == cardapio_id
    assert [i.nome for i in db_session.query(ItemCardapio).all()] == ["Lentilha"]
    preservadas = client.get("/equipe/reclamacoes/", headers=equipe_headers).json()
    assert [r["descricao"] for r in preservadas] == ["Texto preservado."]
