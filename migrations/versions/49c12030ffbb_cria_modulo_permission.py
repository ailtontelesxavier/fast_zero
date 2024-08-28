"""cria modulo permission

Revision ID: 49c12030ffbb
Revises: c180c69014fa
Create Date: 2024-08-28 17:16:51.447994

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '49c12030ffbb'
down_revision: Union[str, None] = 'c180c69014fa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Inserção de um módulo inicial
    op.execute(
        sa.text("INSERT INTO module (id, title) VALUES (3, 'Permission')")
    )


def downgrade() -> None:
    # Remoção do módulo inicial
    op.execute(
        sa.text("DELETE FROM module WHERE title='Permission'")
    )