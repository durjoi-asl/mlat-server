"""empty message

Revision ID: 7f63dc7da0ca
Revises: 767011f4cd9c
Create Date: 2021-10-04 15:46:32.429427

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7f63dc7da0ca'
down_revision = '767011f4cd9c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'admin')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('admin', sa.BOOLEAN(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###