import sqlalchemy as sa
from alembic import command

from tests.test_migracao_identidade import configurar_alembic

REVISAO_ANTERIOR = "5a6b7c8d9e0f"


def test_migracao_adiciona_e_remove_dados_da_ultima_importacao(tmp_path):
    url_banco = f"sqlite:///{tmp_path / 'migracao.db'}"
    engine = sa.create_engine(url_banco)
    metadados = sa.MetaData()
    sa.Table(
        "campus",
        metadados,
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("nome", sa.String(length=100), nullable=False, unique=True),
    )
    metadados.create_all(engine)
    with engine.begin() as conexao:
        conexao.execute(sa.text("INSERT INTO campus (id, nome) VALUES (1, 'Gama')"))

    config = configurar_alembic(url_banco)
    command.stamp(config, REVISAO_ANTERIOR)
    command.upgrade(config, "head")

    colunas = {coluna["name"] for coluna in sa.inspect(engine).get_columns("campus")}
    assert {"ultima_importacao_em", "ultima_fonte_pdf_url"} <= colunas
    with engine.connect() as conexao:
        registro = conexao.execute(
            sa.text(
                "SELECT ultima_importacao_em, ultima_fonte_pdf_url FROM campus WHERE id = 1"
            )
        ).one()
    assert registro == (None, None)

    command.downgrade(config, REVISAO_ANTERIOR)

    colunas = {
        coluna["name"]
        for coluna in sa.inspect(sa.create_engine(url_banco)).get_columns("campus")
    }
    assert "ultima_importacao_em" not in colunas
    assert "ultima_fonte_pdf_url" not in colunas
