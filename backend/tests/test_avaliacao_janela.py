"""RF04 / CA-RF04-03 / CA-RF04-04 / RN05 / D03 — janela de avaliação.

O almoço do cardápio de teste é de 15/09/2026 e começa às 11h (America/Sao_Paulo);
a janela fecha às 00h de 16/09/2026.
"""

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models import Avaliacao
from tests.test_cardapio_api import IDENTIDADE_1, IDENTIDADE_2, criar_cardapio_de_teste


def _avaliar(client: TestClient, cardapio_id: int, nota: int = 4, identidade: str = IDENTIDADE_1):
    return client.post(
        f"/cardapios/{cardapio_id}/avaliacoes/",
        headers={"X-Identidade": identidade},
        json={"nota": nota},
    )


def test_antes_do_inicio_recusa_com_mensagem(client: TestClient, db_session: Session, definir_agora):
    cardapio = criar_cardapio_de_teste(db_session)
    definir_agora(2026, 9, 15, 10, 59, 59)

    response = _avaliar(client, cardapio.id)

    assert response.status_code == 422
    assert "a partir do início do serviço" in response.json()["detail"]
    assert db_session.query(Avaliacao).count() == 0


def test_no_inicio_aceita(client: TestClient, db_session: Session, definir_agora):
    cardapio = criar_cardapio_de_teste(db_session)
    definir_agora(2026, 9, 15, 11, 0, 0)

    assert _avaliar(client, cardapio.id).status_code == 201
    assert db_session.query(Avaliacao).count() == 1


def test_um_instante_antes_das_00h_do_dia_seguinte_aceita(
    client: TestClient, db_session: Session, definir_agora
):
    cardapio = criar_cardapio_de_teste(db_session)
    definir_agora(2026, 9, 15, 23, 59, 59)

    assert _avaliar(client, cardapio.id).status_code == 201


def test_as_00h_do_dia_seguinte_recusa_com_mensagem(
    client: TestClient, db_session: Session, definir_agora
):
    cardapio = criar_cardapio_de_teste(db_session)
    definir_agora(2026, 9, 16, 0, 0, 0)

    response = _avaliar(client, cardapio.id)

    assert response.status_code == 422
    assert "00h do dia seguinte" in response.json()["detail"]
    assert db_session.query(Avaliacao).count() == 0


def test_refeicao_inexistente_recusa(client: TestClient, db_session: Session, definir_agora):
    definir_agora(2026, 9, 15, 12)

    response = _avaliar(client, 999)

    assert response.status_code == 404
    assert db_session.query(Avaliacao).count() == 0


def test_mesma_identidade_e_refeicao_atualiza_sem_criar_segunda(
    client: TestClient, db_session: Session, definir_agora
):
    cardapio = criar_cardapio_de_teste(db_session)
    definir_agora(2026, 9, 15, 12)
    primeira = _avaliar(client, cardapio.id, nota=2)

    definir_agora(2026, 9, 15, 20)
    segunda = _avaliar(client, cardapio.id, nota=5)

    assert (primeira.status_code, segunda.status_code) == (201, 200)
    assert segunda.json()["id"] == primeira.json()["id"]
    assert segunda.json()["nota"] == 5
    assert db_session.query(Avaliacao).count() == 1
    assert _avaliar(client, cardapio.id, identidade=IDENTIDADE_2).status_code == 201
    assert db_session.query(Avaliacao).count() == 2


def test_atualizacao_fora_da_janela_tambem_e_recusada(
    client: TestClient, db_session: Session, definir_agora
):
    cardapio = criar_cardapio_de_teste(db_session)
    definir_agora(2026, 9, 15, 12)
    _avaliar(client, cardapio.id, nota=3)

    definir_agora(2026, 9, 16, 0)
    response = _avaliar(client, cardapio.id, nota=1)

    assert response.status_code == 422
    db_session.expire_all()
    assert db_session.query(Avaliacao).one().nota == 3
