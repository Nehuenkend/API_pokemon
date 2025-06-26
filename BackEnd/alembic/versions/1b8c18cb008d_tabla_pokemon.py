"""tabla pokemon

Revision ID: 1b8c18cb008d
Revises:
Create Date: 2025-06-25 19:21:14.917440

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "1b8c18cb008d"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "pokemon",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("nombre", sa.Text, nullable=False),
        sa.Column("imagen", sa.Float, nullable=False),
        sa.Column("altura", sa.Text, nullable=False),
        sa.Column("peso", sa.Float, nullable=False),
        sa.Column("estadisticas", sa.BLOB, nullable=False),
        sa.Column("evoluciones", sa.BLOB),
    )


def downgrade() -> None:
    op.drop_table("pokemon")
