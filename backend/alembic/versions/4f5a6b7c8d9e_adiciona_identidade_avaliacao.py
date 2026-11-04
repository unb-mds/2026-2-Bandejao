"""adiciona identidade anonima a avaliacao

Revision ID: 4f5a6b7c8d9e
Revises: cb27a92c83d1
Create Date: 2026-10-15
"""

from typing import Sequence, Union
from uuid import uuid4

from alembic import op
import sqlalchemy as sa


revision: str = "4f5a6b7c8d9e"
down_revision: Union[str, None] = "cb27a92c83d1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "avaliacao",
        sa.Column("identidade", sa.Uuid(), nullable=True),
    )

    avaliacao = sa.table(
        "avaliacao",
        sa.column("id", sa.Integer()),
        sa.column("identidade", sa.Uuid()),
    )
    conexao = op.get_bind()
    for avaliacao_id in conexao.execute(sa.select(avaliacao.c.id)).scalars():
        conexao.execute(
            avaliacao.update()
            .where(avaliacao.c.id == avaliacao_id)
            .values(identidade=uuid4())
        )

    with op.batch_alter_table("avaliacao") as batch_op:
        batch_op.alter_column(
            "identidade",
            existing_type=sa.Uuid(),
            nullable=False,
        )
        batch_op.create_unique_constraint(
            "uq_avaliacao_cardapio_identidade",
            ["cardapio_id", "identidade"],
        )


def downgrade() -> None:
    with op.batch_alter_table("avaliacao") as batch_op:
        batch_op.drop_constraint(
            "uq_avaliacao_cardapio_identidade",
            type_="unique",
        )
        batch_op.drop_column("identidade")
