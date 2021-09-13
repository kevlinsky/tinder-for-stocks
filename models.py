from sqlalchemy import String, Integer, Boolean, Numeric, Date
from sqlalchemy.sql.schema import Column, ForeignKey
from db import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=False)
    updates_subscribed = Column(Boolean, default=False)


class Stock(Base):
    __tablename__ = 'stocks'

    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True, nullable=False)
    market_link = Column(String(255), nullable=False)
    currency = Column(String(3), nullable=False)
    market_sector = Column(String(255), nullable=False)
    region = Column(String(255), nullable=False)
    index = Column(String(10), nullable=False)
    market_cap = Column(Numeric, nullable=False)
    ebitda = Column(Numeric, nullable=False)
    debt_equity = Column(Numeric, nullable=False)
    p_e = Column(Numeric, nullable=False)
    roa = Column(Numeric, nullable=False)
    roe = Column(Numeric, nullable=False)
    beta = Column(Numeric, nullable=False)
    revenue = Column(Numeric, nullable=False)
    debt = Column(Numeric, nullable=False)
    expenses = Column(Numeric, nullable=False)
    price = Column(Numeric, nullable=False)
    figi = Column(Numeric, nullable=False)


class Screener(Base):
    __tablename__ = 'screeners'

    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True, nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id', ondelete='RESTRICT'), nullable=False)
    public = Column(Boolean, default=False, nullable=False)
    currency = Column(String(9), nullable=False)
    market_sector = Column(String(1000), nullable=False)
    region = Column(String(1000), nullable=False)
    index = Column(String(1000), nullable=False)
    market_cap = Column(String(1000), nullable=False)
    ebitda = Column(String(1000), nullable=False)
    debt_equity = Column(String(1000), nullable=False)
    p_e = Column(String(1000), nullable=False)
    roa = Column(String(1000), nullable=False)
    roe = Column(String(1000), nullable=False)
    beta = Column(String(1000), nullable=False)
    revenue = Column(String(1000), nullable=False)
    debt = Column(String(1000), nullable=False)
    expenses = Column(String(1000), nullable=False)
    price = Column(String(1000), nullable=False)


class UserFavoriteStock(Base):
    __tablename__ = 'users_favorite_stocks'

    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    stock_id = Column(Integer, ForeignKey('stocks.id', ondelete='CASCADE'), nullable=False)


class UserStockNotifier(Base):
    __tablename__ = 'users_stocks_notifiers'

    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True, nullable=False)
    stock_id = Column(Integer, ForeignKey('stocks.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    target_price = Column(Numeric, nullable=False)


class UserScreener(Base):
    __tablename__ = 'users_screeners'

    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    screener_id = Column(Integer, ForeignKey('screeners.id', ondelete='CASCADE'), nullable=False)
