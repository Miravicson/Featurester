"""empty message

Revision ID: f22f705b2f01
Revises: 65ce600c41ad
Create Date: 2018-12-12 16:59:20.333468

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f22f705b2f01'
down_revision = '65ce600c41ad'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('feature', 'client_priority',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('feature', 'client_priority',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###