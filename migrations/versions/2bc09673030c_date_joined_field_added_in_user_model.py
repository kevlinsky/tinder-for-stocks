"""date_joined field added in User model

Revision ID: 2bc09673030c
Revises: 61c2447e2581
Create Date: 2021-10-07 16:25:28.816167

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2bc09673030c'
down_revision = '61c2447e2581'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('date_joined', sa.Date(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'date_joined')
    # ### end Alembic commands ###
