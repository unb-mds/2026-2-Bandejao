from pathlib import Path

from alembic import command
from alembic.config import Config
import sqlalchemy as sa

from app.core.config import settings


REVISAO_ANTERIOR = "cb27a92c83d1"
REVISAO_INICIAL = "3e9ed9bb9055"


def configurar_alembic(url_banco: str) -> Config:
    raiz_backend = Path(__file__).resolve().parents[1]
    config = Config(raiz_backend / "alembic.ini")
    config.set_main_option("script_location", str(raiz_backend / "alembic"))
    settings.database_url = url_banco
    return config


def test_migracao_adiciona_identidade_e_permite_downgrade(tmp_path):
    url_banco = f"sqlite:///{tmp_path / 'migracao.db'}"
    config = configurar_alembic(url_banco)
    command.upgrade(config, REVISAO_INICIAL)

    engine = sa.create_engine(url_banco)
    with engine.begin() as conexao:
        # Reproduz em SQLite o estado da revisão anterior. A revisão de amendoim
        # remove um default com ALTER COLUMN, sintaxe que existe no PostgreSQL.
        conexao.execute(
            sa.text(
                "ALTER TABLE item_cardapio "
                "ADD COLUMN contem_amendoim BOOLEAN NOT NULL DEFAULT 0"
            )
        )
    command.stamp(config, REVISAO_ANTERIOR)

    with engine.begin() as conexao:
        conexao.execute(sa.text("INSERT INTO campus (id, nome) VALUES (1, 'Gama')"))
        conexao.execute(
            sa.text(
                "INSERT INTO cardapio "
                "(id, campus_id, data, tipo_refeicao) "
                "VALUES (1, 1, '2026-10-15', 'ALMOCO')"
            )
        )
        conexao.execute(
            sa.text(
                "INSERT INTO avaliacao "
                "(id, cardapio_id, nota, comentario, criado_em) "
                "VALUES (1, 1, 4, 'Registro anterior', CURRENT_TIMESTAMP)"
            )
        )

    command.upgrade(config, "head")

    inspetor = sa.inspect(engine)
    assert "identidade" in {coluna["name"] for coluna in inspetor.get_columns("avaliacao")}
    assert {"cardapio_id", "identidade"} in [
        set(restricao["column_names"])
        for restricao in inspetor.get_unique_constraints("avaliacao")
    ]
    with engine.connect() as conexao:
        identidade = conexao.scalar(sa.text("SELECT identidade FROM avaliacao WHERE id = 1"))
    assert identidade is not None

    command.downgrade(config, REVISAO_ANTERIOR)

    inspetor = sa.inspect(sa.create_engine(url_banco))
    assert "identidade" not in {
        coluna["name"] for coluna in inspetor.get_columns("avaliacao")
    }
    with engine.connect() as conexao:
        assert conexao.scalar(sa.text("SELECT count(*) FROM avaliacao")) == 1
