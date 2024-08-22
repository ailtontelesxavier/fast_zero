"""update

Revision ID: 668395663852
Revises: f1675151ead5
Create Date: 2024-08-14 13:16:08.067505

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '668395663852'
down_revision: Union[str, None] = 'f1675151ead5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('parcelamento_negociacao', 'type',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('parcelamento_negociacao', 'type',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###