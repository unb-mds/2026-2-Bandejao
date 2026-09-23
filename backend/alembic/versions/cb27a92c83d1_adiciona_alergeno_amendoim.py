"""adiciona alergeno amendoim

Revision ID: cb27a92c83d1
Revises: 3e9ed9bb9055
Create Date: 2026-09-22
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "cb27a92c83d1"
down_revision: Union[str, None] = "3e9ed9bb9055"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # O valor padrão preserva os registros já existentes durante a evolução do schema.
    op.add_column(
        "item_cardapio",
        sa.Column("contem_amendoim", sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    op.alter_column("item_cardapio", "contem_amendoim", server_default=None)


def downgrade() -> None:
    op.drop_column("item_cardapio", "contem_amendoim")
