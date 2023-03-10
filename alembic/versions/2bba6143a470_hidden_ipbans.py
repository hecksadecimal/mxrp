"""hidden ipbans

Revision ID: 2bba6143a470
Revises: 418d40c91e2e
Create Date: 2016-03-14 00:11:22.093854

"""

# revision identifiers, used by Alembic.
revision = '2bba6143a470'
down_revision = '418d40c91e2e'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ip_bans', sa.Column('hidden', sa.Boolean(), nullable=False, server_default='false'))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('ip_bans', 'hidden')
    ### end Alembic commands ###
