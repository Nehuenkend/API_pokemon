"""tabla intermedia pokemon movimiento nivel

Revision ID: f0b1ba483e03
Revises: 625d98cb9997
Create Date: 2025-06-25 19:37:24.000353

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f0b1ba483e03"
down_revision: Union[str, Sequence[str], None] = "625d98cb9997"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "pokemonmovimientonivel",
        sa.Column(
            "pokemon_id", sa.Integer, sa.ForeignKey("pokemon.id"), primary_key=True
        ),
        sa.Column(
            "movimiento_id",
            sa.Integer,
            sa.ForeignKey("movimiento.id"),
            primary_key=True,
        ),
    )


def downgrade() -> None:
    op.drop_table("pokemonmovimientonivel")
