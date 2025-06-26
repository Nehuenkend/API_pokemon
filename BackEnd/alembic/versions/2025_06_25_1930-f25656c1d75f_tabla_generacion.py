"""tabla generacion

Revision ID: f25656c1d75f
Revises: 1b8c18cb008d
Create Date: 2025-06-25 19:30:15.917796

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f25656c1d75f"
down_revision: Union[str, Sequence[str], None] = "1b8c18cb008d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "generacion",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("nombre", sa.Text, nullable=False),
    )


def downgrade() -> None:
    op.drop_table("generacion")
