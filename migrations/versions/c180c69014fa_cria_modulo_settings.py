"""cria modulo settings

Revision ID: c180c69014fa
Revises: 99629cac53f3
Create Date: 2024-08-28 17:15:06.731338

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c180c69014fa'
down_revision: Union[str, None] = '99629cac53f3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Inserção de um módulo inicial
    op.execute(
        sa.text("INSERT INTO module (id, title) VALUES (2, 'Settings')")
    )


def downgrade() -> None:
    # Remoção do módulo inicial
    op.execute(
        sa.text("DELETE FROM module WHERE title='Settings'")
    )
