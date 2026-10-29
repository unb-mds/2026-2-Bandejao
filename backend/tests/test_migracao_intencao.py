from uuid import UUID

import pytest
import sqlalchemy as sa
from alembic import command
from alembic.autogenerate import compare_metadata
from alembic.migration import MigrationContext
from sqlalchemy.schema import CreateTable

from app.db.session import Base
from tests.test_cardapio_api import IDENTIDADE_1
from tests.test_migracao_identidade import REVISAO_ANTERIOR, REVISAO_INICIAL, configurar_alembic

REVISAO_IMPORTACAO = "6b7c8d9e0f1a"


def test_migracao_intencao_preserva_legados_e_aplica_defaults_unique_e_relacao(tmp_path):
    config = configurar_alembic(f"sqlite:///{tmp_path / 'intencao.db'}")
    command.upgrade(config, REVISAO_INICIAL)
    engine = sa.create_engine(f"sqlite:///{tmp_path / 'intencao.db'}")
    with engine.begin() as conexao:
        conexao.execute(sa.text(
            "ALTER TABLE item_cardapio ADD COLUMN contem_amendoim BOOLEAN NOT NULL DEFAULT 0"
        ))
    command.stamp(config, REVISAO_ANTERIOR)
    command.upgrade(config, REVISAO_IMPORTACAO)
    with engine.begin() as conexao:
        conexao.execute(sa.text("INSERT INTO campus (id,nome) VALUES (1,'Gama')"))
        conexao.execute(sa.text(
            "INSERT INTO cardapio (id,campus_id,data,tipo_refeicao) "
            "VALUES (1,1,'2026-09-15','ALMOCO')"
        ))
        conexao.execute(sa.text(
            "INSERT INTO checkin (id,campus_id,criado_em) VALUES (1,1,CURRENT_TIMESTAMP)"
        ))

    command.upgrade(config, "head")
    inspetor = sa.inspect(engine)
    assert "intencao" in inspetor.get_table_names()
    colunas = {c["name"]: c for c in inspetor.get_columns("intencao")}
    assert set(colunas) == {"id", "cardapio_id", "identidade", "ativa", "simulada"}
    assert all(not c["nullable"] for c in colunas.values())
    assert {"cardapio_id", "identidade"} in [
        set(c["column_names"]) for c in inspetor.get_unique_constraints("intencao")
    ]
    assert inspetor.get_foreign_keys("intencao")[0]["options"]["ondelete"] == "CASCADE"
    with engine.connect() as conexao:
        diferencas = compare_metadata(MigrationContext.configure(conexao), Base.metadata)
        assert [d for d in diferencas if "intencao" in str(d)] == []
    with engine.begin() as conexao:
        conexao.execute(sa.text(
            "INSERT INTO intencao (cardapio_id,identidade) VALUES (1,:identidade)"
        ), {"identidade": UUID(IDENTIDADE_1).hex})
        assert conexao.execute(sa.text("SELECT ativa,simulada FROM intencao")).one() == (1, 0)
    with pytest.raises(sa.exc.IntegrityError), engine.begin() as conexao:
        conexao.execute(sa.text(
            "INSERT INTO intencao (cardapio_id,identidade) VALUES (1,:identidade)"
        ), {"identidade": UUID(IDENTIDADE_1).hex})
    command.downgrade(config, REVISAO_IMPORTACAO)
    assert "intencao" not in sa.inspect(engine).get_table_names()
    with engine.connect() as conexao:
        assert conexao.scalar(sa.text("SELECT count(*) FROM cardapio")) == 1
        assert conexao.scalar(sa.text("SELECT count(*) FROM checkin")) == 1


def test_modelo_intencao_compila_para_postgresql():
    from sqlalchemy.dialects import postgresql

    from app.models import Intencao

    sql = str(CreateTable(Intencao.__table__).compile(dialect=postgresql.dialect()))
    assert "identidade UUID NOT NULL" in sql
    assert "ativa BOOLEAN DEFAULT true NOT NULL" in sql
    assert "simulada BOOLEAN DEFAULT false NOT NULL" in sql
    assert "UNIQUE (cardapio_id, identidade)" in sql
