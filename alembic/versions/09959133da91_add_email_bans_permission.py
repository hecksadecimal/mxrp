"""Add email_bans permission.

Revision ID: 09959133da91
Revises: 1678892f1bd4
Create Date: 2017-02-13 23:42:01.226422

"""

# revision identifiers, used by Alembic.
revision = '09959133da91'
down_revision = '1678892f1bd4'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.execute('COMMIT;')
    op.execute('ALTER TYPE admin_tier_permissions_permission ADD VALUE \'email_bans\';')
    op.execute('INSERT INTO admin_tier_permissions (admin_tier_id, permission) VALUES (1, \'email_bans\');')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###
