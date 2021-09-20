from sqlalchemy import String, Integer, Boolean
from sqlalchemy.sql.schema import Column, ForeignKey
from app.db import ModelAdmin, Base


class Screener(Base, ModelAdmin):
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
