from sqlalchemy import String, Integer, Boolean, Numeric, select, Enum, DateTime, Date
from sqlalchemy.sql.schema import Column, ForeignKey
import enum
import datetime

from app.db import Base, async_db_session, ModelAdmin


class User(Base, ModelAdmin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=False)
    updates_subscribed = Column(Boolean, default=False)
    date_joined = Column(Date, default=datetime.datetime.now())

    @classmethod
    async def get_by_email(cls, email):
        query = select(cls).where(cls.email == email)
        results = (await async_db_session.execute(query)).scalars().all()
        result = None
        if len(results) > 0:
            result = results[0]
        return result


class UserFavoriteStock(Base, ModelAdmin):
    __tablename__ = 'users_favorite_stocks'

    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    stock_id = Column(Integer, ForeignKey('stocks.id', ondelete='CASCADE'), nullable=False)


class UserStockNotifier(Base, ModelAdmin):
    __tablename__ = 'users_stocks_notifiers'

    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True, nullable=False)
    stock_id = Column(Integer, ForeignKey('stocks.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    target_price = Column(Numeric, nullable=False)


class UserScreener(Base, ModelAdmin):
    __tablename__ = 'users_screeners'

    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    screener_id = Column(Integer, ForeignKey('screeners.id', ondelete='CASCADE'), nullable=False)

    @classmethod
    async def get_users_screeners(cls, user_id):
        query = select(cls).where(cls.user_id == user_id)
        results = (await async_db_session.execute(query)).scalars().all()
        return results


class CodeTargetEnum(enum.Enum):
    EMAIL_VERIFICATION = 'email_verification'
    PASSWORD_RESET = 'password_reset'


class UserCode(Base, ModelAdmin):
    __tablename__ = 'users_codes'

    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    code = Column(Integer, nullable=False)
    target = Column(Enum(CodeTargetEnum))
    datetime = Column(DateTime, default=datetime.datetime.now())

    @classmethod
    async def get_by_user_and_target(cls, user_id, target):
        query = select(cls).where(cls.user_id == user_id, cls.target == target)
        results = (await async_db_session.execute(query)).scalars().all()
        result = None
        if len(results) > 0:
            result = results[0]
        return result
