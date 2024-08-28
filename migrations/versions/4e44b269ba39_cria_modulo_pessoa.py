"""cria modulo pessoa

Revision ID: 4e44b269ba39
Revises: 49c12030ffbb
Create Date: 2024-08-28 17:17:52.984182

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4e44b269ba39'
down_revision: Union[str, None] = '49c12030ffbb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Inserção de um módulo inicial
    op.execute(
        sa.text("INSERT INTO module (id, title) VALUES (4, 'Pessoa')")
    )


def downgrade() -> None:
    # Remoção do módulo inicial
    op.execute(
        sa.text("DELETE FROM module WHERE title='Pessoa'")
    )

