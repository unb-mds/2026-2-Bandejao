"""cria tabela de reclamacoes

Revision ID: 5a6b7c8d9e0f
Revises: 4f5a6b7c8d9e
Create Date: 2026-10-21
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "5a6b7c8d9e0f"
down_revision: Union[str, None] = "4f5a6b7c8d9e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "reclamacao",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("cardapio_id", sa.Integer(), nullable=False),
        sa.Column("identidade", sa.Uuid(), nullable=False),
        sa.Column(
            "categoria",
            sa.Enum("QUALIDADE", "HIGIENE", "ATENDIMENTO", "OUTROS", name="categoria_reclamacao"),
            nullable=False,
        ),
        sa.Column("descricao", sa.String(length=1000), nullable=False),
        sa.Column("criado_em", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["cardapio_id"], ["cardapio.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("reclamacao")
    # O tipo enum é próprio do PostgreSQL; em outros bancos a chamada não faz nada.
    sa.Enum(name="categoria_reclamacao").drop(op.get_bind(), checkfirst=True)
