from datetime import UTC, date

import pytest
from fastapi.testclient import TestClient
from pydantic import SecretStr
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models import (
    Avaliacao,
    Campus,
    Cardapio,
    Categoria,
    ItemCardapio,
    TipoDieta,
    TipoRefeicao,
)


IDENTIDADE_1 = "123e4567-e89b-42d3-a456-426614174000"
IDENTIDADE_2 = "123e4567-e89b-42d3-a456-426614174001"


@pytest.fixture()
def importacao_headers(monkeypatch):
    monkeypatch.setattr(settings, "importacao_token", SecretStr("segredo-apenas-para-teste"))
    return {"Authorization": "Bearer segredo-apenas-para-teste"}


def criar_cardapio_de_teste(db_session: Session) -> Cardapio:
    # Esta massa combina item comum, item com alérgenos e opção vegetariana para os filtros.
    campus = Campus(nome="Gama")
    db_session.add(campus)
    db_session.flush()

    cardapio = Cardapio(
        campus_id=campus.id,
        data=date(2026, 9, 15),
        tipo_refeicao=TipoRefeicao.ALMOCO,
    )
    db_session.add(cardapio)
    db_session.flush()
    db_session.add_all(
        [
            ItemCardapio(
                cardapio_id=cardapio.id,
                categoria=Categoria.ACOMPANHAMENTO,
                tipo_dieta=TipoDieta.COMUM,
                nome="Arroz",
            ),
            ItemCardapio(
                cardapio_id=cardapio.id,
                categoria=Categoria.PRATO_PRINCIPAL,
                tipo_dieta=TipoDieta.PADRAO,
                nome="Frango grelhado",
            ),
            ItemCardapio(
                cardapio_id=cardapio.id,
                categoria=Categoria.SOBREMESA,
                tipo_dieta=TipoDieta.OVOLACTOVEGETARIANO,
                nome="Bolo de fubá",
                contem_gluten=True,
                contem_leite=True,
                contem_ovo=True,
            ),
            ItemCardapio(
                cardapio_id=cardapio.id,
                categoria=Categoria.FRUTA,
                tipo_dieta=TipoDieta.VEGETARIANO_ESTRITO,
                nome="Banana",
            ),
        ]
    )
    db_session.commit()
    return cardapio


@pytest.mark.parametrize(
    ("tipo_dieta", "nomes_esperados"),
    [
        ("comum", ["Arroz"]),
        ("padrao", ["Frango grelhado"]),
        ("ovolactovegetariano", ["Bolo de fubá", "Banana"]),
        ("vegetariano_estrito", ["Banana"]),
    ],
)
def test_filtro_de_dieta_inclui_apenas_classes_compativeis(
    client: TestClient,
    db_session: Session,
    tipo_dieta: str,
    nomes_esperados: list[str],
):
    criar_cardapio_de_teste(db_session)

    response = client.get("/cardapios/", params={"tipo_dieta": tipo_dieta})

    assert response.status_code == 200
    assert [item["nome"] for item in response.json()[0]["itens"]] == nomes_esperados


def test_lista_campi_ordenados(client: TestClient, db_session: Session):
    db_session.add_all([Campus(nome="Planaltina"), Campus(nome="Ceilândia")])
    db_session.commit()

    response = client.get("/campi/")

    assert response.status_code == 200
    assert [campus["nome"] for campus in response.json()] == ["Ceilândia", "Planaltina"]


def test_cors_permite_metodos_e_identidade_do_frontend(client: TestClient):
    response = client.options(
        "/cardapios/1/avaliacoes/",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "Content-Type,X-Identidade",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:5173"
    metodos = response.headers["access-control-allow-methods"]
    for metodo in ["GET", "POST", "PUT", "DELETE", "OPTIONS"]:
        assert metodo in metodos
    assert "x-identidade" in response.headers["access-control-allow-headers"].lower()


def test_obtem_campus_e_retorna_404_quando_nao_existe(client: TestClient, db_session: Session):
    campus = Campus(nome="Darcy Ribeiro")
    db_session.add(campus)
    db_session.commit()

    response = client.get(f"/campi/{campus.id}")

    assert response.status_code == 200
    assert response.json() == {
        "id": campus.id,
        "nome": "Darcy Ribeiro",
        "ultima_importacao_em": None,
        "ultima_fonte_pdf_url": None,
    }
    assert client.get("/campi/999").status_code == 404


def test_lista_cardapio_filtra_por_campus_dieta_e_alergeno(
    client: TestClient, db_session: Session
):
    cardapio = criar_cardapio_de_teste(db_session)

    response = client.get(
        "/cardapios/",
        params={
            "campus_id": cardapio.campus_id,
            "tipo_dieta": "vegetariano_estrito",
            "excluir_alergenos": "gluten",
        },
    )

    assert response.status_code == 200
    resultado = response.json()
    assert len(resultado) == 1
    assert resultado[0]["id"] == cardapio.id
    assert resultado[0]["campus_id"] == cardapio.campus_id
    assert [item["nome"] for item in resultado[0]["itens"]] == ["Banana"]


def test_lista_e_obtem_cardapio_com_filtros_de_data_e_refeicao(
    client: TestClient, db_session: Session
):
    cardapio = criar_cardapio_de_teste(db_session)

    response = client.get(
        "/cardapios/",
        params={
            "data_inicio": "2026-09-15",
            "data_fim": "2026-09-15",
            "tipo_refeicao": "almoco",
        },
    )

    assert response.status_code == 200
    assert [resultado["id"] for resultado in response.json()] == [cardapio.id]
    assert client.get(f"/cardapios/{cardapio.id}").status_code == 200
    assert client.get("/cardapios/999").status_code == 404


def test_rejeita_alergeno_desconhecido(client: TestClient):
    response = client.get("/cardapios/", params={"excluir_alergenos": "desconhecido"})

    assert response.status_code == 400
    assert "Alérgeno inválido" in response.json()["detail"]


def test_importa_cardapio_e_substitui_itens_ao_reprocessar(
    client: TestClient, db_session: Session, importacao_headers, definir_agora
):
    definir_agora(2026, 10, 24, 9, 30)
    payload = {
        "campus": "Gama",
        "fonte_pdf_url": "https://ru.unb.br/gama-semana.pdf",
        "refeicoes": [
            {
                "data": "2026-09-21",
                "tipo_refeicao": "almoco",
                "itens": [
                    {
                        "categoria": "prato_principal",
                        "tipo_dieta": "padrao",
                        "nome": "Frango grelhado",
                        "alergenos": ["amendoim", "soja"],
                    }
                ],
            }
        ],
    }

    primeira_resposta = client.post("/cardapios/importacao", json=payload, headers=importacao_headers)
    assert primeira_resposta.status_code == 200
    assert primeira_resposta.json()["itens_processados"] == 1
    assert primeira_resposta.json()["ultima_importacao_em"] == "2026-10-24T12:30:00Z"
    assert primeira_resposta.json()["fonte_pdf_url"] == payload["fonte_pdf_url"]
    campus_api = client.get("/campi/").json()[0]
    assert campus_api["ultima_importacao_em"] == "2026-10-24T12:30:00Z"
    assert campus_api["ultima_fonte_pdf_url"] == payload["fonte_pdf_url"]
    assert client.get("/cardapios/", params={"excluir_alergenos": "amendoim"}).json()[0][
        "itens"
    ] == []

    payload["refeicoes"][0]["itens"][0]["nome"] = "Lentilha"
    payload["refeicoes"][0]["itens"][0]["alergenos"] = []
    payload["fonte_pdf_url"] = "https://ru.unb.br/gama-semana-corrigida.pdf"
    definir_agora(2026, 10, 24, 15, 45)
    segunda_resposta = client.post("/cardapios/importacao", json=payload, headers=importacao_headers)

    assert segunda_resposta.status_code == 200
    assert segunda_resposta.json()["ultima_importacao_em"] == "2026-10-24T18:45:00Z"
    assert segunda_resposta.json()["fonte_pdf_url"] == payload["fonte_pdf_url"]
    assert db_session.query(Campus).filter_by(nome="Gama").count() == 1
    cardapio = db_session.query(Cardapio).filter_by(data=date(2026, 9, 21)).one()
    assert [(item.nome, item.contem_soja, item.contem_amendoim) for item in cardapio.itens] == [
        ("Lentilha", False, False)
    ]


def test_falha_de_importacao_preserva_ultimo_sucesso(
    client: TestClient, db_session: Session, importacao_headers, definir_agora
):
    campus = Campus(
        nome="Gama",
        ultima_importacao_em=definir_agora(2026, 10, 24, 9).astimezone(UTC),
        ultima_fonte_pdf_url="https://ru.unb.br/ultima-fonte-valida.pdf",
    )
    db_session.add(campus)
    db_session.commit()
    definir_agora(2026, 10, 24, 16)

    response = client.post(
        "/cardapios/importacao",
        headers=importacao_headers,
        json={
            "campus": "Gama",
            "fonte_pdf_url": "https://ru.unb.br/fonte-com-falha.pdf",
            "refeicoes": [
                {
                    "data": "2026-10-24",
                    "tipo_refeicao": "almoco",
                    "itens": [
                        {
                            "categoria": "sobremesa",
                            "tipo_dieta": "comum",
                            "nome": "Pudim",
                            "alergenos": ["desconhecido"],
                        }
                    ],
                }
            ],
        },
    )

    assert response.status_code == 422
    campus_api = client.get(f"/campi/{campus.id}").json()
    assert campus_api["ultima_importacao_em"] == "2026-10-24T12:00:00Z"
    assert campus_api["ultima_fonte_pdf_url"] == "https://ru.unb.br/ultima-fonte-valida.pdf"


def test_importacao_rejeita_alergeno_fora_do_contrato(client: TestClient, importacao_headers):
    response = client.post(
        "/cardapios/importacao",
        headers=importacao_headers,
        json={
            "campus": "Gama",
            "refeicoes": [
                {
                    "data": "2026-09-21",
                    "tipo_refeicao": "almoco",
                    "itens": [
                        {
                            "categoria": "sobremesa",
                            "tipo_dieta": "comum",
                            "nome": "Pudim",
                            "alergenos": ["desconhecido"],
                        }
                    ],
                }
            ],
        },
    )

    assert response.status_code == 422


def test_cria_avaliacao_para_cardapio_existente(
    client: TestClient, db_session: Session, definir_agora
):
    definir_agora(2026, 9, 15, 12)
    cardapio = criar_cardapio_de_teste(db_session)

    response = client.post(
        f"/cardapios/{cardapio.id}/avaliacoes/",
        headers={"X-Identidade": IDENTIDADE_1},
        json={"nota": 5, "comentario": "Ótima refeição."},
    )

    assert response.status_code == 201
    assert response.json()["cardapio_id"] == cardapio.id
    assert response.json()["nota"] == 5
    assert response.json()["comentario"] == "Ótima refeição."
    assert "identidade" not in response.json()
    avaliacoes = client.get(f"/cardapios/{cardapio.id}/avaliacoes/").json()
    assert avaliacoes[0]["id"] == response.json()["id"]
    assert all("identidade" not in avaliacao for avaliacao in avaliacoes)
    assert client.get("/cardapios/999/avaliacoes/").status_code == 404


def test_nova_avaliacao_da_mesma_identidade_atualiza_sem_duplicar(
    client: TestClient, db_session: Session, definir_agora
):
    definir_agora(2026, 9, 15, 12)
    cardapio = criar_cardapio_de_teste(db_session)
    url = f"/cardapios/{cardapio.id}/avaliacoes/"
    headers = {"X-Identidade": IDENTIDADE_1}

    primeira = client.post(url, headers=headers, json={"nota": 2, "comentario": "Regular"})
    atualizada = client.post(url, headers=headers, json={"nota": 5, "comentario": "Melhorou"})

    assert primeira.status_code == 201
    assert atualizada.status_code == 200
    assert atualizada.json()["id"] == primeira.json()["id"]
    assert atualizada.json()["nota"] == 5
    assert atualizada.json()["comentario"] == "Melhorou"
    assert db_session.query(Avaliacao).count() == 1


def test_identidades_diferentes_criam_avaliacoes_separadas(
    client: TestClient, db_session: Session, definir_agora
):
    definir_agora(2026, 9, 15, 12)
    cardapio = criar_cardapio_de_teste(db_session)
    url = f"/cardapios/{cardapio.id}/avaliacoes/"

    primeira = client.post(
        url,
        headers={"X-Identidade": IDENTIDADE_1},
        json={"nota": 4},
    )
    segunda = client.post(
        url,
        headers={"X-Identidade": IDENTIDADE_2},
        json={"nota": 3},
    )

    assert primeira.status_code == 201
    assert segunda.status_code == 201
    assert primeira.json()["id"] != segunda.json()["id"]
    assert db_session.query(Avaliacao).count() == 2


@pytest.mark.parametrize(
    "identidade",
    [None, "nao-e-uuid", "6ba7b810-9dad-11d1-80b4-00c04fd430c8"],
)
def test_rejeita_identidade_ausente_invalida_ou_fora_da_versao_4(
    client: TestClient, db_session: Session, identidade
):
    cardapio = criar_cardapio_de_teste(db_session)
    headers = {} if identidade is None else {"X-Identidade": identidade}

    response = client.post(
        f"/cardapios/{cardapio.id}/avaliacoes/",
        headers=headers,
        json={"nota": 4},
    )

    assert response.status_code == 400
    assert "UUID v4" in response.json()["detail"]
    assert db_session.query(Avaliacao).count() == 0


def test_rejeita_nota_fora_do_intervalo(client: TestClient, db_session: Session):
    cardapio = criar_cardapio_de_teste(db_session)

    response = client.post(
        f"/cardapios/{cardapio.id}/avaliacoes/",
        headers={"X-Identidade": IDENTIDADE_1},
        json={"nota": 6},
    )

    assert response.status_code == 422


def test_checkins_legados_nao_estao_expostos(client: TestClient, db_session: Session):
    campus = Campus(nome="Fazenda Água Limpa")
    db_session.add(campus)
    db_session.commit()

    response = client.post(f"/campi/{campus.id}/checkins/")

    assert response.status_code == 404
    assert client.get(f"/campi/{campus.id}/checkins/").status_code == 404
    assert client.post("/campi/999/checkins/").status_code == 404


@pytest.mark.parametrize("authorization", [None, "Bearer incorreto", "Basic incorreto", "Bearer"])
def test_importacao_sem_credencial_valida_nao_grava(
    client: TestClient, db_session: Session, importacao_headers, authorization
):
    cardapio = criar_cardapio_de_teste(db_session)
    headers = {} if authorization is None else {"Authorization": authorization}
    response = client.post(
        "/cardapios/importacao",
        headers=headers,
        json={
            "campus": "Gama",
            "refeicoes": [{"data": "2026-09-15", "tipo_refeicao": "almoco", "itens": []}],
        },
    )
    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"
    db_session.expire_all()
    assert db_session.query(Campus).count() == 1
    assert db_session.query(Cardapio).count() == 1
    assert len(db_session.get(Cardapio, cardapio.id).itens) == 4
    assert "segredo-apenas-para-teste" not in response.text


@pytest.mark.parametrize("token_configurado", ["", "   "])
def test_importacao_sem_segredo_configurado_falha_fechada(
    client: TestClient, db_session: Session, monkeypatch, token_configurado
):
    monkeypatch.setattr(settings, "importacao_token", SecretStr(token_configurado))
    response = client.post(
        "/cardapios/importacao",
        headers={"Authorization": "Bearer qualquer-token"},
        json={"campus": "Gama", "refeicoes": []},
    )
    assert response.status_code == 401
    assert db_session.query(Campus).count() == 0
    assert db_session.query(Cardapio).count() == 0
    assert db_session.query(ItemCardapio).count() == 0
    assert client.get("/cardapios/").status_code == 200
    assert client.get("/campi/").status_code == 200
