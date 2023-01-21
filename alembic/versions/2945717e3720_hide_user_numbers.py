"""hide user numbers

Revision ID: 2945717e3720
Revises: f8acbd22162
Create Date: 2016-01-31 00:43:02.777003

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column

# revision identifiers, used by Alembic.
revision = '2945717e3720'
down_revision = 'f8acbd22162'
branch_labels = None
depends_on = None


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('chat_users', sa.Column('show_user_numbers', sa.Boolean(), nullable=False, server_default='true'))
    op.add_column('users', sa.Column('show_user_numbers', sa.Boolean(), nullable=False, server_default='true'))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'show_user_numbers')
    op.drop_column('chat_users', 'show_user_numbers')
    ### end Alembic commands ###
