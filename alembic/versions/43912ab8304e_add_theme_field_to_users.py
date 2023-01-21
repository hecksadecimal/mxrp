"""Add theme field to users.

Revision ID: 43912ab8304e
Revises: 2a777b3adf25
Create Date: 2015-09-18 22:30:19.735772

"""

# revision identifiers, used by Alembic.
revision = '43912ab8304e'
down_revision = '2a777b3adf25'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('theme', sa.Unicode(length=255), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'theme')
    ### end Alembic commands ###
