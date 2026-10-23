import sqlalchemy as sa
from alembic import command
from alembic.autogenerate import compare_metadata
from alembic.migration import MigrationContext

from app.db.session import Base
from tests.test_migracao_identidade import REVISAO_ANTERIOR, REVISAO_INICIAL, configurar_alembic

REVISAO_IDENTIDADE = "4f5a6b7c8d9e"


def test_migracao_cria_e_remove_a_tabela_de_reclamacoes(tmp_path):
    url_banco = f"sqlite:///{tmp_path / 'migracao.db'}"
    config = configurar_alembic(url_banco)
    command.upgrade(config, REVISAO_INICIAL)
    engine = sa.create_engine(url_banco)
    with engine.begin() as conexao:
        # Mesmo contorno do teste de identidade: a revisão do amendoim usa ALTER COLUMN.
        conexao.execute(
            sa.text(
                "ALTER TABLE item_cardapio "
                "ADD COLUMN contem_amendoim BOOLEAN NOT NULL DEFAULT 0"
            )
        )
    command.stamp(config, REVISAO_ANTERIOR)
    command.upgrade(config, REVISAO_IDENTIDADE)
    assert "reclamacao" not in sa.inspect(engine).get_table_names()

    command.upgrade(config, "head")

    inspetor = sa.inspect(engine)
    assert "reclamacao" in inspetor.get_table_names()
    colunas = {coluna["name"]: coluna for coluna in inspetor.get_columns("reclamacao")}
    assert set(colunas) == {
        "id",
        "cardapio_id",
        "identidade",
        "categoria",
        "descricao",
        "criado_em",
    }
    assert all(not coluna["nullable"] for coluna in colunas.values())
    # O banco migrado precisa ficar igual ao que os modelos descrevem para essa tabela.
    with engine.connect() as conexao:
        diferencas = compare_metadata(MigrationContext.configure(conexao), Base.metadata)
    assert [d for d in diferencas if "reclamacao" in str(d)] == []

    command.downgrade(config, REVISAO_IDENTIDADE)

    assert "reclamacao" not in sa.inspect(sa.create_engine(url_banco)).get_table_names()
