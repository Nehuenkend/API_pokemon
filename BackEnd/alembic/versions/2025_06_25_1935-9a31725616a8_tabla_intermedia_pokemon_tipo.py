"""tabla intermedia pokemon tipo

Revision ID: 9a31725616a8
Revises: e95dd1ee1f03
Create Date: 2025-06-25 19:35:10.950694

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9a31725616a8"
down_revision: Union[str, Sequence[str], None] = "e95dd1ee1f03"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "pokemontipo",
        sa.Column(
            "pokemon_id", sa.Integer, sa.ForeignKey("pokemon.id"), primary_key=True
        ),
        sa.Column("tipo_id", sa.Integer, sa.ForeignKey("tipo.id"), primary_key=True),
    )


def downgrade() -> None:
    op.drop_table("pokemontipo")
