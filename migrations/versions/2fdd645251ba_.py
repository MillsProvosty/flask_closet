"""empty message

Revision ID: 2fdd645251ba
Revises: 
Create Date: 2020-06-03 16:00:57.028003

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2fdd645251ba'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=300), nullable=True),
    sa.Column('clothing_type', sa.String(length=100), nullable=True),
    sa.Column('occasion', sa.String(length=100), nullable=True),
    sa.Column('color', sa.String(length=100), nullable=True),
    sa.Column('season', sa.String(length=100), nullable=True),
    sa.Column('image', sa.String(length=500), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('person',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=200), nullable=True),
    sa.Column('email', sa.String(length=200), nullable=True),
    sa.Column('password', sa.String(length=500), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('person')
    op.drop_table('item')
    # ### end Alembic commands ###
