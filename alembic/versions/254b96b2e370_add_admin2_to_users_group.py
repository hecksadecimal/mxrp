"""Add 'admin2' to users_group.

Revision ID: 254b96b2e370
Revises: 40975dd21696
Create Date: 2015-09-23 19:24:39.902455

"""

# revision identifiers, used by Alembic.
revision = '254b96b2e370'
down_revision = '40975dd21696'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.execute('COMMIT;')
    op.execute('ALTER TYPE users_group ADD VALUE \'admin1\';')
    op.execute('UPDATE users SET "group"=\'admin1\' WHERE "group"=\'admin\';')
    op.execute('ALTER TYPE users_group ADD VALUE \'admin2\';')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###
