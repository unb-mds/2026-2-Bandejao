"""RF06: intenção pessoal, sem horário de chegada e com prazo em Brasília."""

from datetime import UTC, date, datetime
from uuid import UUID

import pytest
from sqlalchemy.exc import IntegrityError

from app.core.tempo import agora
from app.main import app
from app.models import Cardapio
from tests.test_cardapio_api import IDENTIDADE_1, IDENTIDADE_2, criar_cardapio_de_teste

HEADERS = {"X-Identidade": IDENTIDADE_1}


@pytest.fixture()
def cardapio(db_session, definir_agora):
    definir_agora(2026, 9, 15, 10, 59, 59)
    return criar_cardapio_de_teste(db_session)


def test_marcar_ler_desmarcar_e_remarcar_sem_duplicar(client, db_session, cardapio):
    url = f"/cardapios/{cardapio.id}/intencao/"
    assert client.get(url, headers=HEADERS).json() == {
        "cardapio_id": cardapio.id, "ativa": False
    }
    for _ in range(2):
        resposta = client.put(url, headers=HEADERS)
        assert resposta.status_code == 200
        assert resposta.json() == {"cardapio_id": cardapio.id, "ativa": True}
        assert IDENTIDADE_1 not in resposta.text
    assert client.get(url, headers=HEADERS).json()["ativa"] is True
    for _ in range(2):
        resposta = client.delete(url, headers=HEADERS)
        assert resposta.status_code == 200
        assert resposta.json() == {"cardapio_id": cardapio.id, "ativa": False}
    assert client.put(url, headers=HEADERS).json()["ativa"] is True
    from app.models import Intencao

    assert db_session.query(Intencao).count() == 1
    registro = db_session.query(Intencao).one()
    assert registro.cardapio == cardapio
    assert cardapio.intencoes == [registro]
    assert registro.simulada is False
    assert registro.identidade == UUID(IDENTIDADE_1)


@pytest.mark.parametrize("metodo", ["get", "put", "delete"])
def test_refeicao_ausente_e_identidade_invalida(client, metodo):
    requisitar = getattr(client, metodo)
    assert requisitar("/cardapios/999/intencao/", headers=HEADERS).status_code == 404
    for identidade in [None, "invalida", "6ba7b810-9dad-11d1-80b4-00c04fd430c8"]:
        headers = {} if identidade is None else {"X-Identidade": identidade}
        resposta = requisitar("/cardapios/999/intencao/", headers=headers)
        assert resposta.status_code == 400
        assert "UUID v4" in resposta.json()["detail"]


@pytest.mark.parametrize("hora,minuto,segundo", [(11, 0, 0), (11, 0, 1), (23, 59, 59)])
def test_recusa_no_inicio_ou_depois_sem_reativar(
    client, db_session, cardapio, definir_agora, hora, minuto, segundo
):
    url = f"/cardapios/{cardapio.id}/intencao/"
    assert client.put(url, headers=HEADERS).status_code == 200
    assert client.delete(url, headers=HEADERS).status_code == 200
    definir_agora(2026, 9, 15, hora, minuto, segundo)
    resposta = client.put(url, headers=HEADERS)
    assert resposta.status_code == 422
    assert "início do serviço" in resposta.json()["detail"]
    assert client.get(url, headers=HEADERS).json()["ativa"] is False


def test_cancelar_apos_prazo_e_repetir_ausencia_nao_cria_linha(
    client, db_session, cardapio, definir_agora
):
    from app.models import Intencao

    url = f"/cardapios/{cardapio.id}/intencao/"
    client.put(url, headers=HEADERS)
    definir_agora(2026, 9, 16)
    assert client.put(url, headers=HEADERS).status_code == 422
    assert client.delete(url, headers=HEADERS).json()["ativa"] is False
    assert client.delete(url, headers={"X-Identidade": IDENTIDADE_2}).json()["ativa"] is False
    assert db_session.query(Intencao).count() == 1


def test_prazo_usa_fuso_brasilia_e_permite_marcar_no_dia_anterior(client, cardapio):
    url = f"/cardapios/{cardapio.id}/intencao/"
    for instante, status in [
        (datetime(2026, 9, 14, 23, tzinfo=UTC), 200),
        (datetime(2026, 9, 15, 13, 59, 59, tzinfo=UTC), 200),
        (datetime(2026, 9, 15, 14, tzinfo=UTC), 422),
    ]:
        app.dependency_overrides[agora] = lambda: instante
        assert client.put(url, headers=HEADERS).status_code == status


def test_ignora_flag_simulada_do_cliente(client, db_session, cardapio):
    from app.models import Intencao

    resposta = client.put(
        f"/cardapios/{cardapio.id}/intencao/", headers=HEADERS,
        json={"simulada": True, "horario_chegada": "10:30"},
    )
    assert resposta.status_code == 200
    assert db_session.query(Intencao).one().simulada is False


def test_identidades_isoladas_e_sem_cache(client, cardapio):
    url = f"/cardapios/{cardapio.id}/intencao/"
    client.put(url, headers=HEADERS)
    outro = {"X-Identidade": IDENTIDADE_2}
    assert client.get(url, headers=outro).json()["ativa"] is False
    assert client.delete(url, headers=outro).json()["ativa"] is False
    for caminho in [url, "/intencoes/"]:
        resposta = client.get(caminho, headers=HEADERS)
        assert resposta.headers["cache-control"] == "no-store"
        assert IDENTIDADE_1 not in resposta.text
    assert client.get(url, headers=HEADERS).json()["ativa"] is True


def test_banco_impede_duplicacao_inclusive_cancelada(db_session, cardapio):
    from app.models import Intencao

    db_session.add(Intencao(cardapio_id=cardapio.id, identidade=UUID(IDENTIDADE_1), ativa=False))
    db_session.commit()
    db_session.add(Intencao(cardapio_id=cardapio.id, identidade=UUID(IDENTIDADE_1)))
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()


@pytest.mark.parametrize("params", [
    {"data_inicio": "2026-09-14"}, {"data_fim": "2026-09-20"},
    {"data_inicio": "2026-09-20", "data_fim": "2026-09-14"},
    {"data_inicio": "15/09/2026", "data_fim": "2026-09-20"},
    {"data_inicio": "1790000000", "data_fim": "2026-09-20"},
    {"data_inicio": "2026-09-14T00:00:00", "data_fim": "2026-09-20"},
    {"data_inicio": "2026-02-30", "data_fim": "2026-09-20"},
    {"campus_id": "abc"}, {"campus_id": 0},
])
def test_listagem_valida_intervalo_sem_ambiguidade(client, params):
    assert client.get("/intencoes/", params=params, headers=HEADERS).status_code == 422


def test_listagem_exige_identidade(client):
    assert client.get("/intencoes/").status_code == 400


def test_listagem_filtra_ativas_reais_campus_datas_e_ordena(client, db_session, cardapio):
    from app.models import Campus, Intencao, TipoRefeicao

    outro_campus = Campus(nome="Darcy Ribeiro")
    db_session.add(outro_campus)
    db_session.flush()
    refeicoes = [cardapio]
    for campus_id, dia, tipo in [
        (cardapio.campus_id, 14, TipoRefeicao.ALMOCO),
        (cardapio.campus_id, 20, TipoRefeicao.JANTAR),
        (cardapio.campus_id, 13, TipoRefeicao.ALMOCO),
        (cardapio.campus_id, 21, TipoRefeicao.ALMOCO),
        (outro_campus.id, 15, TipoRefeicao.ALMOCO),
        (cardapio.campus_id, 15, TipoRefeicao.JANTAR),
        (cardapio.campus_id, 16, TipoRefeicao.ALMOCO),
    ]:
        refeicao = Cardapio(campus_id=campus_id, data=date(2026, 9, dia), tipo_refeicao=tipo)
        db_session.add(refeicao)
        db_session.flush()
        refeicoes.append(refeicao)
    for indice, refeicao in enumerate(refeicoes):
        db_session.add(Intencao(
            cardapio_id=refeicao.id, identidade=UUID(IDENTIDADE_1),
            ativa=indice != 6, simulada=indice == 7,
        ))
    db_session.add(Intencao(cardapio_id=cardapio.id, identidade=UUID(IDENTIDADE_2)))
    db_session.commit()
    resposta = client.get("/intencoes/", headers=HEADERS)
    assert resposta.status_code == 200
    assert [i["cardapio_id"] for i in resposta.json()] == [
        refeicoes[i].id for i in [1, 0, 5, 2]
    ]
    assert resposta.json()[1] == {
        "cardapio_id": cardapio.id, "campus_id": cardapio.campus_id,
        "data": "2026-09-15", "tipo_refeicao": "almoco", "ativa": True,
    }
    assert IDENTIDADE_1 not in resposta.text
    filtrada = client.get("/intencoes/", headers=HEADERS, params={
        "campus_id": cardapio.campus_id, "data_inicio": "2026-09-15",
        "data_fim": "2026-09-15",
    })
    assert [i["cardapio_id"] for i in filtrada.json()] == [cardapio.id]
    assert client.get("/intencoes/", headers=HEADERS, params={"campus_id": 999}).json() == []


def test_semana_padrao_converte_utc_para_brasilia(client, db_session, cardapio):
    client.put(f"/cardapios/{cardapio.id}/intencao/", headers=HEADERS)
    app.dependency_overrides[agora] = lambda: datetime(2026, 9, 21, 1, tzinfo=UTC)
    assert len(client.get("/intencoes/", headers=HEADERS).json()) == 1
    app.dependency_overrides[agora] = lambda: datetime(2026, 9, 21, 3, tzinfo=UTC)
    assert client.get("/intencoes/", headers=HEADERS).json() == []


def test_simulada_nao_aparece_na_consulta_pessoal_nem_e_alterada(client, db_session, cardapio):
    from app.models import Intencao

    registro = Intencao(cardapio_id=cardapio.id, identidade=UUID(IDENTIDADE_1), simulada=True)
    db_session.add(registro)
    db_session.commit()
    url = f"/cardapios/{cardapio.id}/intencao/"
    assert client.get(url, headers=HEADERS).json()["ativa"] is False
    assert client.get("/intencoes/", headers=HEADERS).json() == []
    assert client.delete(url, headers=HEADERS).json()["ativa"] is False
    assert client.put(url, headers=HEADERS).status_code == 409
    db_session.refresh(registro)
    assert registro.simulada is True
    assert registro.ativa is True


def test_sem_horario_configurado_recusa_marcacao(client, cardapio, monkeypatch):
    from app.api.routes import intencao

    monkeypatch.setattr(intencao, "HORARIOS_INICIO_REFEICAO", {})
    resposta = client.put(f"/cardapios/{cardapio.id}/intencao/", headers=HEADERS)
    assert resposta.status_code == 422
    assert "não configurado" in resposta.json()["detail"]


@pytest.mark.parametrize("tipo,hora", [("cafe_da_manha", 7), ("almoco", 11), ("jantar", 17)])
def test_prazo_de_cada_refeicao(client, db_session, cardapio, definir_agora, tipo, hora):
    from app.models import TipoRefeicao

    cardapio.tipo_refeicao = TipoRefeicao(tipo)
    db_session.commit()
    url = f"/cardapios/{cardapio.id}/intencao/"
    definir_agora(2026, 9, 15, hora - 1, 59, 59)
    assert client.put(url, headers=HEADERS).status_code == 200
    definir_agora(2026, 9, 15, hora)
    assert client.put(url, headers=HEADERS).status_code == 422


def test_reimportacao_preserva_intencoes_ativas_e_canceladas(
    client, db_session, cardapio, monkeypatch
):
    from pydantic import SecretStr

    from app.core.config import settings
    from app.models import Intencao

    url = f"/cardapios/{cardapio.id}/intencao/"
    outro = {"X-Identidade": IDENTIDADE_2}
    client.put(url, headers=HEADERS)
    client.put(url, headers=outro)
    client.delete(url, headers=outro)
    estados = [(i.id, i.ativa) for i in db_session.query(Intencao).order_by(Intencao.id)]
    monkeypatch.setattr(settings, "importacao_token", SecretStr("token-teste"))
    for _ in range(2):
        resposta = client.post("/cardapios/importacao", headers={
            "Authorization": "Bearer token-teste"
        }, json={"campus": "Gama", "refeicoes": [{
            "data": "2026-09-15", "tipo_refeicao": "almoco", "itens": []
        }]})
        assert resposta.status_code == 200
    db_session.expire_all()
    assert [(i.id, i.ativa) for i in db_session.query(Intencao).order_by(Intencao.id)] == estados
    assert db_session.query(Cardapio).one().id == cardapio.id


def test_marcacoes_concorrentes_nao_duplicam_nem_falham(tmp_path, monkeypatch):
    from concurrent.futures import ThreadPoolExecutor
    from threading import Barrier, local

    from sqlalchemy import create_engine
    from sqlalchemy.orm import Session

    from app.api.routes import intencao
    from app.core.tempo import FUSO_BRASILIA
    from app.db.session import Base
    from app.models import Intencao

    engine = create_engine(f"sqlite:///{tmp_path / 'concorrencia.db'}")
    Base.metadata.create_all(engine)
    with Session(engine) as db:
        cardapio_id = criar_cardapio_de_teste(db).id
    barreira = Barrier(2)
    chamadas = local()
    consultar = intencao._obter_intencao

    def consultar_com_barreira(*args):
        registro = consultar(*args)
        if not getattr(chamadas, "consultou", False):
            chamadas.consultou = True
            assert registro is None
            barreira.wait(timeout=10)
        return registro

    monkeypatch.setattr(intencao, "_obter_intencao", consultar_com_barreira)

    def marcar(_):
        with Session(engine) as db:
            return intencao.marcar_intencao(
                cardapio_id, UUID(IDENTIDADE_1), db,
                datetime(2026, 9, 15, 10, tzinfo=FUSO_BRASILIA),
            )

    with ThreadPoolExecutor(max_workers=2) as executor:
        resultados = list(executor.map(marcar, range(2)))
    assert all(resultado.ativa for resultado in resultados)
    with Session(engine) as db:
        assert db.query(Intencao).count() == 1
        assert db.query(Intencao).one().ativa is True
    engine.dispose()


def test_falha_de_integridade_inesperada_nao_e_ocultada(client, db_session, cardapio, monkeypatch):
    def falhar():
        raise IntegrityError("falha inesperada", {}, ValueError("falha"))

    monkeypatch.setattr(db_session, "commit", falhar)
    with pytest.raises(IntegrityError, match="falha inesperada"):
        client.put(f"/cardapios/{cardapio.id}/intencao/", headers=HEADERS)
