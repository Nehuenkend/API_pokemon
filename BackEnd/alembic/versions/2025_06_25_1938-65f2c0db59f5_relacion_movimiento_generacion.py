"""relacion movimiento generacion

Revision ID: 65f2c0db59f5
Revises: f0b1ba483e03
Create Date: 2025-06-25 19:38:27.557301

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "65f2c0db59f5"
down_revision: Union[str, Sequence[str], None] = "f0b1ba483e03"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("movimiento") as batch_op:
        batch_op.add_column(sa.Column("id_generacion", sa.Integer))
        batch_op.create_foreign_key(
            "fk_movimiento_generacion",
            "Generacion",
            ["id_generacion"],
            ["id"],
        )


def downgrade() -> None:
    with op.batch_alter_table("movimiento") as batch_op:
        batch_op.drop_constraint("fk_movimiento_generacion", type_="foreignkey")
        batch_op.drop_column("id_generacion")
