from datetime import date

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models import Campus, Cardapio, Categoria, ItemCardapio, TipoDieta, TipoRefeicao


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


def test_lista_campi_ordenados(client: TestClient, db_session: Session):
    db_session.add_all([Campus(nome="Planaltina"), Campus(nome="Ceilândia")])
    db_session.commit()

    response = client.get("/campi/")

    assert response.status_code == 200
    assert [campus["nome"] for campus in response.json()] == ["Ceilândia", "Planaltina"]


def test_obtem_campus_e_retorna_404_quando_nao_existe(client: TestClient, db_session: Session):
    campus = Campus(nome="Darcy Ribeiro")
    db_session.add(campus)
    db_session.commit()

    response = client.get(f"/campi/{campus.id}")

    assert response.status_code == 200
    assert response.json() == {"id": campus.id, "nome": "Darcy Ribeiro"}
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
    client: TestClient, db_session: Session
):
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

    primeira_resposta = client.post("/cardapios/importacao", json=payload)
    assert primeira_resposta.status_code == 200
    assert primeira_resposta.json()["itens_processados"] == 1
    assert client.get("/cardapios/", params={"excluir_alergenos": "amendoim"}).json()[0][
        "itens"
    ] == []

    payload["refeicoes"][0]["itens"][0]["nome"] = "Lentilha"
    payload["refeicoes"][0]["itens"][0]["alergenos"] = []
    segunda_resposta = client.post("/cardapios/importacao", json=payload)

    assert segunda_resposta.status_code == 200
    assert db_session.query(Campus).filter_by(nome="Gama").count() == 1
    cardapio = db_session.query(Cardapio).filter_by(data=date(2026, 9, 21)).one()
    assert [(item.nome, item.contem_soja, item.contem_amendoim) for item in cardapio.itens] == [
        ("Lentilha", False, False)
    ]


def test_importacao_rejeita_alergeno_fora_do_contrato(client: TestClient):
    response = client.post(
        "/cardapios/importacao",
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


def test_cria_avaliacao_para_cardapio_existente(client: TestClient, db_session: Session):
    cardapio = criar_cardapio_de_teste(db_session)

    response = client.post(
        f"/cardapios/{cardapio.id}/avaliacoes/",
        json={"nota": 5, "comentario": "Ótima refeição."},
    )

    assert response.status_code == 201
    assert response.json()["cardapio_id"] == cardapio.id
    assert response.json()["nota"] == 5
    assert response.json()["comentario"] == "Ótima refeição."
    assert client.get(f"/cardapios/{cardapio.id}/avaliacoes/").json()[0]["id"] == response.json()["id"]
    assert client.get("/cardapios/999/avaliacoes/").status_code == 404


def test_rejeita_nota_fora_do_intervalo(client: TestClient, db_session: Session):
    cardapio = criar_cardapio_de_teste(db_session)

    response = client.post(f"/cardapios/{cardapio.id}/avaliacoes/", json={"nota": 6})

    assert response.status_code == 422


def test_registra_e_lista_checkins(client: TestClient, db_session: Session):
    campus = Campus(nome="Fazenda Água Limpa")
    db_session.add(campus)
    db_session.commit()

    response = client.post(f"/campi/{campus.id}/checkins/")

    assert response.status_code == 201
    assert response.json()["campus_id"] == campus.id
    assert len(client.get(f"/campi/{campus.id}/checkins/").json()) == 1
    assert client.post("/campi/999/checkins/").status_code == 404
