"""First migration

Revision ID: e1323553d429
Revises: 32e05b5e907e
Create Date: 2021-01-29 10:34:05.789475

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e1323553d429'
down_revision = '32e05b5e907e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('song', sa.Column('popularity', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('song', 'popularity')
    # ### end Alembic commands ###
