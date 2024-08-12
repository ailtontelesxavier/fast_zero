"""insert inicial module

Revision ID: 8eacd008326a
Revises: 3197a1279fe6
Create Date: 2024-08-12 17:15:24.753602

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8eacd008326a'
down_revision: Union[str, None] = '3197a1279fe6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Inserção de um módulo inicial
    op.execute(
        sa.text("INSERT INTO module (id, title) VALUES (1, 'Juridico')")
    )


def downgrade() -> None:
    # Remoção do módulo inicial
    op.execute(
        sa.text("DELETE FROM module WHERE title='Juridico'")
    )
