"""Verificações que dependem de um PostgreSQL de verdade."""

import os
from uuid import uuid4

import pytest
import sqlalchemy as sa
from alembic import command
from sqlalchemy.engine import make_url

from app.core.config import settings
from tests.test_migracao_identidade import configurar_alembic


def test_engine_de_teste_usa_a_url_postgresql_configurada():
    from tests.conftest import criar_engine_teste

    engine = criar_engine_teste(
        "postgresql+psycopg://bandejao:bandejao@localhost:5432/bandejao"
    )
    try:
        assert engine.dialect.name == "postgresql"
    finally:
        engine.dispose()


@pytest.mark.postgres
def test_migracoes_sobem_e_descem_no_postgresql(monkeypatch):
    url = os.getenv("TEST_DATABASE_URL")
    if not url:
        pytest.skip("Configure TEST_DATABASE_URL para executar no PostgreSQL")

    url_banco = make_url(url)
    if url_banco.get_backend_name() != "postgresql":
        pytest.skip("TEST_DATABASE_URL não aponta para PostgreSQL")

    schema = f"teste_migracao_{uuid4().hex}"
    engine_admin = sa.create_engine(url_banco)
    engine_schema = None
    try:
        with engine_admin.begin() as conexao:
            conexao.exec_driver_sql(f'CREATE SCHEMA "{schema}"')

        url_schema = url_banco.set(
            query={**url_banco.query, "options": f"-csearch_path={schema}"}
        )
        engine_schema = sa.create_engine(url_schema)
        monkeypatch.setattr(settings, "database_url", str(url_schema))
        config = configurar_alembic(str(url_schema))

        command.upgrade(config, "head")

        tabelas = set(sa.inspect(engine_schema).get_table_names())
        assert {
            "alembic_version",
            "avaliacao",
            "campus",
            "cardapio",
            "intencao",
            "item_cardapio",
            "reclamacao",
        } <= tabelas

        command.downgrade(config, "base")
        assert sa.inspect(engine_schema).get_table_names() == []
    finally:
        if engine_schema is not None:
            engine_schema.dispose()
        with engine_admin.begin() as conexao:
            conexao.exec_driver_sql(f'DROP SCHEMA IF EXISTS "{schema}" CASCADE')
        engine_admin.dispose()
