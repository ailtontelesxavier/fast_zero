"""altera parcelamento

Revision ID: 4c28a883bc30
Revises: f1675151ead5
Create Date: 2024-08-14 09:10:22.562351

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4c28a883bc30'
down_revision: Union[str, None] = 'f1675151ead5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('parcelamento_negociacao', sa.Column('type', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('parcelamento_negociacao', 'type')
    # ### end Alembic commands ###
