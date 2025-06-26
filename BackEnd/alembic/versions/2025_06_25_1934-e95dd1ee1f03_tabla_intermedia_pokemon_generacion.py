"""tabla intermedia pokemon generacion

Revision ID: e95dd1ee1f03
Revises: ae6becff1b9d
Create Date: 2025-06-25 19:34:40.504501

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e95dd1ee1f03"
down_revision: Union[str, Sequence[str], None] = "ae6becff1b9d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "pokemongeneracion",
        sa.Column(
            "pokemon_id",
            sa.Integer,
            sa.ForeignKey("pokemon.id"),
            primary_key=True,
        ),
        sa.Column(
            "generacion_id",
            sa.Integer,
            sa.ForeignKey("generacion.id"),
            primary_key=True,
        ),
    )


def downgrade() -> None:
    op.drop_table("pokemongeneracion")
