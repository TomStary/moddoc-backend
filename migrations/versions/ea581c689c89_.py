"""empty message

Revision ID: ea581c689c89
Revises: 208413064373
Create Date: 2019-04-05 18:13:09.462742

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ea581c689c89'
down_revision = '208413064373'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('role', schema=None) as batch_op:
        batch_op.add_column(sa.Column('flag', sa.Integer(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('role', schema=None) as batch_op:
        batch_op.drop_column('flag')

    # ### end Alembic commands ###