"""Add EmailBan table.

Revision ID: cac1f275a725
Revises: 231e2c1e26da
Create Date: 2016-12-12 23:41:56.438144

"""

# revision identifiers, used by Alembic.
revision = 'cac1f275a725'
down_revision = '231e2c1e26da'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('email_bans',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('pattern', sa.Unicode(length=255), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('creator_id', sa.Integer(), nullable=False),
    sa.Column('reason', sa.Unicode(length=255), nullable=False),
    sa.ForeignKeyConstraint(['creator_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('pattern')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('email_host_bans')
    ### end Alembic commands ###
