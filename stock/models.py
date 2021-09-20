from sqlalchemy import String, Integer, Numeric
from sqlalchemy.sql.schema import Column
from app.db import ModelAdmin, Base


class Stock(Base, ModelAdmin):
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
