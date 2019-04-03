"""empty message

Revision ID: 48adbf2a32db
Revises: ab94e6efffa4
Create Date: 2019-04-03 21:44:29.340992

"""
from alembic import op
import sqlalchemy as sa
from moddoc.utils import GUID


# revision identifiers, used by Alembic.
revision = '48adbf2a32db'
down_revision = 'ab94e6efffa4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_to_role',
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.Column('deleted', sa.DateTime(), nullable=True),
    sa.Column('id', GUID(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_to_role')
    # ### end Alembic commands ###