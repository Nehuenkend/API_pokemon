"""tabla movimiento

Revision ID: 3c024722ff2f
Revises: f25656c1d75f
Create Date: 2025-06-25 19:31:21.667570

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3c024722ff2f"
down_revision: Union[str, Sequence[str], None] = "f25656c1d75f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "movimiento",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("nombre", sa.Text, nullable=False),
        sa.Column("categoria", sa.Text, nullable=False),
        sa.Column("potencia", sa.Integer, nullable=True),
        sa.Column("precision", sa.Integer, nullable=True),
        sa.Column("pp", sa.Integer, nullable=True),
        sa.Column("efecto", sa.Text, nullable=False),
        sa.Column("tipo", sa.BLOB, nullable=False),
    )


def downgrade() -> None:
    op.drop_table("movimiento")
