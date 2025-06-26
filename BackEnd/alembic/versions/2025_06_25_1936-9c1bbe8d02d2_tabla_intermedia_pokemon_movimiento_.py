"""tabla intermedia pokemon movimiento maquina

Revision ID: 9c1bbe8d02d2
Revises: bd4769ae7c15
Create Date: 2025-06-25 19:36:14.814678

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9c1bbe8d02d2"
down_revision: Union[str, Sequence[str], None] = "bd4769ae7c15"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "pokemonmovimientomaquina",
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
    op.drop_table("pokemonmovimientomaquina")
