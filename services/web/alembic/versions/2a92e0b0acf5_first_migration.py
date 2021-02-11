"""First migration

Revision ID: 2a92e0b0acf5
Revises: e1323553d429
Create Date: 2021-01-30 09:17:58.437816

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2a92e0b0acf5'
down_revision = 'e1323553d429'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'song', ['spotify_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'song', type_='unique')
    # ### end Alembic commands ###