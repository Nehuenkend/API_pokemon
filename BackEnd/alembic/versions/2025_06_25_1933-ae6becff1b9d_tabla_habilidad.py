"""tabla habilidad

Revision ID: ae6becff1b9d
Revises: f9f5263aae8c
Create Date: 2025-06-25 19:33:08.211775

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ae6becff1b9d"
down_revision: Union[str, Sequence[str], None] = "f9f5263aae8c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "habilidad",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("nombre", sa.String, nullable=False),
    )


def downgrade() -> None:
    op.drop_table("habilidad")
