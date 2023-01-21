"""IP bans table.

Revision ID: 2a777b3adf25
Revises: 55eb2a993f60
Create Date: 2015-09-09 22:24:45.129147

"""

# revision identifiers, used by Alembic.
revision = '2a777b3adf25'
down_revision = '55eb2a993f60'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ip_bans',
    sa.Column('address', postgresql.INET(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('creator_id', sa.Integer(), nullable=False),
    sa.Column('reason', sa.Unicode(length=255), nullable=False),
    sa.ForeignKeyConstraint(['creator_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('address')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ip_bans')
    ### end Alembic commands ###
