"""tabla tipo

Revision ID: f9f5263aae8c
Revises: 3c024722ff2f
Create Date: 2025-06-25 19:31:42.134986

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f9f5263aae8c"
down_revision: Union[str, Sequence[str], None] = "3c024722ff2f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "tipo",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("nombre", sa.String, nullable=False),
        sa.Column("debilidades", sa.BLOB, nullable=False),
    )


def downgrade() -> None:
    op.drop_table("tipo")
