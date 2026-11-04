"""registra ultima importacao bem-sucedida por campus

Revision ID: 6b7c8d9e0f1a
Revises: 5a6b7c8d9e0f
Create Date: 2026-10-24
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "6b7c8d9e0f1a"
down_revision: Union[str, None] = "5a6b7c8d9e0f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "campus",
        sa.Column("ultima_importacao_em", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        "campus",
        sa.Column("ultima_fonte_pdf_url", sa.String(length=500), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("campus", "ultima_fonte_pdf_url")
    op.drop_column("campus", "ultima_importacao_em")
