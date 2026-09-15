from datetime import date

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models import Campus, Cardapio, Categoria, ItemCardapio, TipoDieta, TipoRefeicao


def criar_cardapio_de_teste(db_session: Session) -> Cardapio:
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


def test_rejeita_alergeno_desconhecido(client: TestClient):
    response = client.get("/cardapios/", params={"excluir_alergenos": "amendoim"})

    assert response.status_code == 400
    assert "Alérgeno inválido" in response.json()["detail"]


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


def test_rejeita_nota_fora_do_intervalo(client: TestClient, db_session: Session):
    cardapio = criar_cardapio_de_teste(db_session)

    response = client.post(f"/cardapios/{cardapio.id}/avaliacoes/", json={"nota": 6})

    assert response.status_code == 422
