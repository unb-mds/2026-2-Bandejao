"""Requisições simultâneas para a mesma identidade e refeição."""

from concurrent.futures import ThreadPoolExecutor
import os
from threading import Barrier
from uuid import UUID

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, sessionmaker

from app.db.session import get_db
from app.main import app
from app.models import Avaliacao, Intencao
from tests.test_cardapio_api import IDENTIDADE_1, criar_cardapio_de_teste

POSTGRESQL_CONFIGURADO = os.getenv("TEST_DATABASE_URL", "").startswith(
    ("postgresql://", "postgresql+")
)
requer_postgresql = pytest.mark.skipif(
    not POSTGRESQL_CONFIGURADO,
    reason="Esta prova de concorrência exige PostgreSQL via TEST_DATABASE_URL",
)


@pytest.fixture()
def cardapio(db_session: Session):
    return criar_cardapio_de_teste(db_session)


@pytest.fixture()
def cliente_sem_excecao(db_session: Session):
    anteriores = app.dependency_overrides.copy()

    def obter_banco():
        yield db_session

    app.dependency_overrides[get_db] = obter_banco
    with TestClient(app, raise_server_exceptions=False) as cliente:
        yield cliente
    app.dependency_overrides.clear()
    app.dependency_overrides.update(anteriores)


@pytest.fixture()
def clientes_independentes(db_session: Session):
    engine = db_session.get_bind()
    criar_sessao = sessionmaker(bind=engine, expire_on_commit=False)
    anteriores = app.dependency_overrides.copy()

    def obter_banco():
        with criar_sessao() as sessao:
            yield sessao

    app.dependency_overrides[get_db] = obter_banco
    cliente_a = TestClient(app, raise_server_exceptions=False)
    cliente_b = TestClient(app, raise_server_exceptions=False)
    try:
        with cliente_a, cliente_b:
            yield engine, cliente_a, cliente_b
    finally:
        app.dependency_overrides.clear()
        app.dependency_overrides.update(anteriores)


def _duas_requisicoes_simultaneas(engine, tabela, clientes, metodo, caminho, corpo=None):
    barreira = Barrier(2)

    def sincronizar_buscas(conexao, cursor, instrucao, parametros, contexto, varios):
        sql = " ".join(instrucao.lower().replace('"', "").split())
        if sql.startswith("select") and f"from {tabela}" in sql:
            barreira.wait(timeout=15)

    event.listen(engine, "after_cursor_execute", sincronizar_buscas)
    try:
        def enviar(cliente):
            argumentos = {"headers": {"X-Identidade": IDENTIDADE_1}}
            if corpo is not None:
                argumentos["json"] = corpo
            return cliente.request(metodo, caminho, **argumentos)

        with ThreadPoolExecutor(max_workers=2) as executor:
            tarefas = [executor.submit(enviar, cliente) for cliente in clientes]
            return [tarefa.result(timeout=30) for tarefa in tarefas]
    finally:
        event.remove(engine, "after_cursor_execute", sincronizar_buscas)


def test_avaliacao_reaproveita_linha_criada_por_requisicao_concorrente(
    cliente_sem_excecao, db_session: Session, cardapio, definir_agora, monkeypatch
):
    definir_agora(2026, 9, 15, 12)
    commit_original = db_session.commit
    primeira_chamada = True

    def commit_com_conflito():
        nonlocal primeira_chamada
        if primeira_chamada:
            primeira_chamada = False
            db_session.rollback()
            db_session.add(
                Avaliacao(
                    cardapio_id=cardapio.id,
                    identidade=UUID(IDENTIDADE_1),
                    nota=2,
                    comentario="Registro concorrente",
                )
            )
            commit_original()
            raise IntegrityError("colisão de unicidade", {}, ValueError("duplicado"))
        commit_original()

    monkeypatch.setattr(db_session, "commit", commit_com_conflito)
    resposta = cliente_sem_excecao.post(
        f"/cardapios/{cardapio.id}/avaliacoes/",
        headers={"X-Identidade": IDENTIDADE_1},
        json={"nota": 5, "comentario": "Nota da requisição concorrente"},
    )

    assert resposta.status_code == 200
    db_session.expire_all()
    avaliacao = db_session.query(Avaliacao).one()
    assert (avaliacao.nota, avaliacao.comentario) == (5, "Nota da requisição concorrente")


def test_falha_de_integridade_sem_linha_concorrente_continua_visivel(
    cliente_sem_excecao, db_session: Session, cardapio, definir_agora, monkeypatch
):
    definir_agora(2026, 9, 15, 12)

    def falhar():
        raise IntegrityError("falha inesperada", {}, ValueError("falha"))

    monkeypatch.setattr(db_session, "commit", falhar)
    resposta = cliente_sem_excecao.post(
        f"/cardapios/{cardapio.id}/avaliacoes/",
        headers={"X-Identidade": IDENTIDADE_1},
        json={"nota": 5},
    )

    assert resposta.status_code == 500
    assert db_session.query(Avaliacao).count() == 0


@requer_postgresql
def test_avaliacoes_simultaneas_da_mesma_identidade_nao_duplicam(
    db_session: Session, cardapio, definir_agora, clientes_independentes
):
    db_session.commit()
    definir_agora(2026, 9, 15, 12)
    engine, clientes = clientes_independentes[0], clientes_independentes[1:]
    respostas = _duas_requisicoes_simultaneas(
        engine,
        "avaliacao",
        clientes,
        "POST",
        f"/cardapios/{cardapio.id}/avaliacoes/",
        {"nota": 4, "comentario": "Requisição simultânea"},
    )

    assert all(resposta.status_code in (200, 201) for resposta in respostas)
    db_session.expire_all()
    assert db_session.query(Avaliacao).filter_by(
        cardapio_id=cardapio.id, identidade=UUID(IDENTIDADE_1)
    ).count() == 1


@requer_postgresql
def test_intencoes_simultaneas_da_mesma_identidade_nao_duplicam(
    db_session: Session, cardapio, definir_agora, clientes_independentes
):
    db_session.commit()
    definir_agora(2026, 9, 15, 10, 59)
    engine, clientes = clientes_independentes[0], clientes_independentes[1:]
    respostas = _duas_requisicoes_simultaneas(
        engine,
        "intencao",
        clientes,
        "PUT",
        f"/cardapios/{cardapio.id}/intencao/",
    )

    assert all(resposta.status_code == 200 for resposta in respostas)
    db_session.expire_all()
    assert db_session.query(Intencao).filter_by(
        cardapio_id=cardapio.id, identidade=UUID(IDENTIDADE_1)
    ).count() == 1
