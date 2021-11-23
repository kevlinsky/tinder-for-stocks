from sqlalchemy import String, Integer, Boolean, select
from sqlalchemy.sql.schema import Column, ForeignKey
from app.db import ModelAdmin, Base, async_db_session


class Screener(Base, ModelAdmin):
    __tablename__ = 'screeners'

    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True, nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id', ondelete='RESTRICT'), nullable=False)
    public = Column(Boolean, default=False, nullable=False)
    currency = Column(String(9), nullable=True)
    market_sector = Column(String(1000), nullable=True)
    region = Column(String(1000), nullable=True)
    index = Column(String(1000), nullable=True)
    market_cap = Column(String(1000), nullable=True)
    ebitda = Column(String(1000), nullable=True)
    debt_equity = Column(String(1000), nullable=True)
    p_e = Column(String(1000), nullable=True)
    roa = Column(String(1000), nullable=True)
    roe = Column(String(1000), nullable=True)
    beta = Column(String(1000), nullable=True)
    revenue = Column(String(1000), nullable=True)
    debt = Column(String(1000), nullable=True)
    expenses = Column(String(1000), nullable=True)
    price = Column(String(1000), nullable=True)

    @classmethod
    async def get_user_screeners(cls, user_id):
        query = select(cls).where(cls.owner_id == user_id)
        results = (await async_db_session.execute(query)).scalars().all()
        return results
