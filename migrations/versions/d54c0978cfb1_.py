"""empty message

Revision ID: d54c0978cfb1
Revises: d1e72cc65419
Create Date: 2019-05-15 19:31:28.385004

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'd54c0978cfb1'
down_revision = 'd1e72cc65419'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('document_permission', schema=None) as batch_op:
        batch_op.drop_column('write')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('document_permission', schema=None) as batch_op:
        batch_op.add_column(sa.Column('write', postgresql.UUID(), autoincrement=False, nullable=False))

    # ### end Alembic commands ###