"""add campo updated_at no User

Revision ID: 0fd53b95b5e5
Revises: 2844dee1e11e
Create Date: 2024-07-03 22:26:25.712314

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0fd53b95b5e5'
down_revision: Union[str, None] = '2844dee1e11e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
