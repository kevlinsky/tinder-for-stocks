"""initial revision

Revision ID: cd940ed39558
Revises: 
Create Date: 2021-11-10 16:13:03.587550

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cd940ed39558'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('stocks',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('market_link', sa.String(length=255), nullable=False),
    sa.Column('currency', sa.String(length=3), nullable=False),
    sa.Column('market_sector', sa.String(length=255), nullable=False),
    sa.Column('region', sa.String(length=255), nullable=False),
    sa.Column('exchange', sa.String(length=10), nullable=False),
    sa.Column('market_cap', sa.Numeric(), nullable=False),
    sa.Column('ebitda', sa.Numeric(), nullable=False),
    sa.Column('debt_equity', sa.Numeric(), nullable=False),
    sa.Column('p_e', sa.Numeric(), nullable=False),
    sa.Column('roa', sa.Numeric(), nullable=False),
    sa.Column('roe', sa.Numeric(), nullable=False),
    sa.Column('beta', sa.Numeric(), nullable=False),
    sa.Column('revenue', sa.Numeric(), nullable=False),
    sa.Column('debt', sa.Numeric(), nullable=False),
    sa.Column('price', sa.Numeric(), nullable=False),
    sa.Column('figi', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_stocks_id'), 'stocks', ['id'], unique=True)
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('first_name', sa.String(length=50), nullable=False),
    sa.Column('last_name', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('updates_subscription_type', sa.Enum('NOT_SUBSCRIBED', 'WEEKLY', 'MONTHLY', name='subscriptiontypeenum'), nullable=True),
    sa.Column('date_joined', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=True)
    op.create_table('screeners',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.Column('public', sa.Boolean(), nullable=False),
    sa.Column('currency', sa.String(length=9), nullable=True),
    sa.Column('market_sector', sa.String(length=1000), nullable=True),
    sa.Column('region', sa.String(length=1000), nullable=True),
    sa.Column('exchange', sa.String(length=1000), nullable=True),
    sa.Column('market_cap', sa.String(length=1000), nullable=True),
    sa.Column('ebitda', sa.String(length=1000), nullable=True),
    sa.Column('debt_equity', sa.String(length=1000), nullable=True),
    sa.Column('p_e', sa.String(length=1000), nullable=True),
    sa.Column('roa', sa.String(length=1000), nullable=True),
    sa.Column('roe', sa.String(length=1000), nullable=True),
    sa.Column('beta', sa.String(length=1000), nullable=True),
    sa.Column('revenue', sa.String(length=1000), nullable=True),
    sa.Column('debt', sa.String(length=1000), nullable=True),
    sa.Column('price', sa.String(length=1000), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_screeners_id'), 'screeners', ['id'], unique=True)
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
    op.create_table('users_favorite_stocks',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('stock_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['stock_id'], ['stocks.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_favorite_stocks_id'), 'users_favorite_stocks', ['id'], unique=True)
    op.create_table('users_stocks_notifiers',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('stock_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('target_price', sa.Numeric(), nullable=False),
    sa.ForeignKeyConstraint(['stock_id'], ['stocks.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_stocks_notifiers_id'), 'users_stocks_notifiers', ['id'], unique=True)
    op.create_table('users_screeners',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('screener_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['screener_id'], ['screeners.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_screeners_id'), 'users_screeners', ['id'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_screeners_id'), table_name='users_screeners')
    op.drop_table('users_screeners')
    op.drop_index(op.f('ix_users_stocks_notifiers_id'), table_name='users_stocks_notifiers')
    op.drop_table('users_stocks_notifiers')
    op.drop_index(op.f('ix_users_favorite_stocks_id'), table_name='users_favorite_stocks')
    op.drop_table('users_favorite_stocks')
    op.drop_index(op.f('ix_users_codes_id'), table_name='users_codes')
    op.drop_table('users_codes')
    op.drop_index(op.f('ix_screeners_id'), table_name='screeners')
    op.drop_table('screeners')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_stocks_id'), table_name='stocks')
    op.drop_table('stocks')
    # ### end Alembic commands ###
