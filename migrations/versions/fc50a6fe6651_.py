"""empty message

Revision ID: fc50a6fe6651
Revises: 1cfa5699c29d
Create Date: 2019-05-15 16:48:30.191276

"""
from alembic import op
import sqlalchemy as sa
from moddoc.utils import GUID


# revision identifiers, used by Alembic.
revision = 'fc50a6fe6651'
down_revision = '1cfa5699c29d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('document_permission',
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.Column('deleted', sa.DateTime(), nullable=True),
    sa.Column('document_id', GUID(), nullable=True),
    sa.Column('user_id', GUID(), nullable=True),
    sa.Column('read', GUID(), nullable=False),
    sa.Column('write', GUID(), nullable=False),
    sa.Column('id', GUID(), nullable=False),
    sa.ForeignKeyConstraint(['document_id'], ['document.id'], name=op.f('fk_document_permission_document_id_document')),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_document_permission_user_id_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_document_permission'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('document_permission')
    # ### end Alembic commands ###