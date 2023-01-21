"""spamless filters

Revision ID: 2ac1e82fa9aa
Revises: 36db9588efa3
Create Date: 2015-11-30 03:25:54.546206

"""

# revision identifiers, used by Alembic.
revision = '2ac1e82fa9aa'
down_revision = '36db9588efa3'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('spamless_filters',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.Enum('banned_names', 'blacklist', 'warnlist', name='spamless_filter_types'), nullable=False),
    sa.Column('regex', sa.UnicodeText(), nullable=False),
    sa.Column('points', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('spamless_filters')
    ### end Alembic commands ###
