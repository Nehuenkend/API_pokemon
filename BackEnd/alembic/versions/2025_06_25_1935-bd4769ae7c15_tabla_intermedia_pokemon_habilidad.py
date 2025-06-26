"""tabla intermedia pokemon habilidad

Revision ID: bd4769ae7c15
Revises: 9a31725616a8
Create Date: 2025-06-25 19:35:40.943587

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "bd4769ae7c15"
down_revision: Union[str, Sequence[str], None] = "9a31725616a8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "pokemonhabilidad",
        sa.Column(
            "pokemon_id", sa.Integer, sa.ForeignKey("pokemon.id"), primary_key=True
        ),
        sa.Column(
            "habilidad_id", sa.Integer, sa.ForeignKey("habilidad.id"), primary_key=True
        ),
    )


def downgrade() -> None:
    op.drop_table("pokemonhabilidad")
