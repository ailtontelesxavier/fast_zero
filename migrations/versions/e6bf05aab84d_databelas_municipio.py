"""databelas municipio

Revision ID: e6bf05aab84d
Revises: f0da87eb25d3
Create Date: 2024-09-09 08:00:56.634261

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e6bf05aab84d'
down_revision: Union[str, None] = 'f0da87eb25d3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('regiao',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nome', sa.String(), nullable=False),
    sa.Column('sigla', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('nome', 'sigla', name='unique_regiao_nome_sigla')
    )
    op.create_table('uf',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('sigla', sa.String(length=2), nullable=False),
    sa.Column('nome', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('sigla')
    )
    op.create_table('municipio',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nome', sa.String(), nullable=False),
    sa.Column('uf_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['uf_id'], ['uf.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_constraint('unique_numero_type_negociacao', 'parcelamento_negociacao', type_='unique')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('unique_numero_type_negociacao', 'parcelamento_negociacao', ['numero_parcela', 'type', 'negociacao_id'])
    op.drop_table('municipio')
    op.drop_table('uf')
    op.drop_table('regiao')
    # ### end Alembic commands ###
