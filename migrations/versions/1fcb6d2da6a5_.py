"""empty message

Revision ID: 1fcb6d2da6a5
Revises: b7648a5aa4b9
Create Date: 2019-04-28 12:12:39.395569

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '1fcb6d2da6a5'
down_revision = 'b7648a5aa4b9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('used_modules')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('used_modules',
    sa.Column('created', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('updated', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('deleted', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('module_id', postgresql.UUID(), autoincrement=False, nullable=False),
    sa.Column('document_id', postgresql.UUID(), autoincrement=False, nullable=False),
    sa.Column('id', postgresql.UUID(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['document_id'], ['document.id'], name='used_modules_document_id_fkey'),
    sa.ForeignKeyConstraint(['module_id'], ['module.id'], name='used_modules_module_id_fkey'),
    sa.PrimaryKeyConstraint('module_id', 'document_id', 'id', name='used_modules_pkey')
    )
    # ### end Alembic commands ###
