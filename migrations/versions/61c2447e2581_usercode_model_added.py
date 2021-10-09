"""UserCode model added

Revision ID: 61c2447e2581
Revises: 37b49892ce8f
Create Date: 2021-09-21 14:22:42.164764

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '61c2447e2581'
down_revision = '37b49892ce8f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users_codes',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('code', sa.Integer(), nullable=False),
    sa.Column('target', sa.Enum('EMAIL_VERIFICATION', 'PASSWORD_RESET', name='codetargetenum'), nullable=True),
    sa.Column('datetime', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_codes_id'), 'users_codes', ['id'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_codes_id'), table_name='users_codes')
    op.drop_table('users_codes')
    # ### end Alembic commands ###