"""empty message

Revision ID: a7bb45c16302
Revises: 8514c9a439e4
Create Date: 2019-04-27 22:48:45.301005

"""
from alembic import op
import sqlalchemy as sa
from moddoc.utils import GUID


# revision identifiers, used by Alembic.
revision = 'a7bb45c16302'
down_revision = '8514c9a439e4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('document',
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.Column('deleted', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('id', GUID(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('revision',
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.Column('deleted', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('id', GUID(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('linked_repositories',
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.Column('deleted', sa.DateTime(), nullable=True),
    sa.Column('repository_id', GUID(), nullable=False),
    sa.Column('document_id', GUID(), nullable=False),
    sa.Column('id', GUID(), nullable=False),
    sa.ForeignKeyConstraint(['document_id'], ['document.id'], ),
    sa.ForeignKeyConstraint(['repository_id'], ['repository.id'], ),
    sa.PrimaryKeyConstraint('repository_id', 'document_id', 'id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('linked_repositories')
    op.drop_table('revision')
    op.drop_table('document')
    # ### end Alembic commands ###