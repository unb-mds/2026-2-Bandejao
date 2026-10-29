"""cria intenções de refeição sem alterar check-ins legados

Revision ID: 7c8d9e0f1a2b
Revises: 6b7c8d9e0f1a
"""

from alembic import op
import sqlalchemy as sa

revision = "7c8d9e0f1a2b"
down_revision = "6b7c8d9e0f1a"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "intencao",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("cardapio_id", sa.Integer(), nullable=False),
        sa.Column("identidade", sa.Uuid(), nullable=False),
        sa.Column("ativa", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("simulada", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.ForeignKeyConstraint(["cardapio_id"], ["cardapio.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("cardapio_id", "identidade", name="uq_intencao_cardapio_identidade"),
    )


def downgrade() -> None:
    op.drop_table("intencao")
