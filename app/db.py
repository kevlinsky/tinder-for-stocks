from sqlalchemy.future import select
from sqlalchemy import delete
from sqlalchemy import update as sqlalchemy_update
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

host = os.getenv('POSTGRES_HOST')
db = os.getenv('POSTGRES_DB')
port = os.getenv('POSTGRES_PORT')
user = os.getenv('POSTGRES_USER')
password = os.getenv('POSTGRES_PASSWORD')

SQLALCHEMY_DATABASE_URL = f'postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}'

Base = declarative_base()


class AsyncDatabaseSession:
    def __init__(self):
        self._engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
        self._session = sessionmaker(self._engine, expire_on_commit=False, class_=AsyncSession)()

    def __getattr__(self, name):
        return getattr(self._session, name)

    async def create_all(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


async_db_session = AsyncDatabaseSession()


def count_iterable(i):
    return sum(1 for e in i)


class ModelAdmin:
    @classmethod
    async def create(cls, **kwargs):
        obj = cls(**kwargs)
        async_db_session.add(obj)
        await async_db_session.commit()
        return obj.id

    @classmethod
    async def update(cls, id, **kwargs):
        query = (
            sqlalchemy_update(cls)
            .where(cls.id == id)
            .values(**kwargs)
            .execution_options(synchronize_session='fetch')
        )

        await async_db_session.execute(query)
        await async_db_session.commit()

    @classmethod
    async def get(cls, id):
        query = select(cls).where(cls.id == id)
        results = (await async_db_session.execute(query)).scalars().all()
        result = None
        if len(results) > 0:
            result = results[0]
        return result

    @classmethod
    async def delete(cls, id):
        query = delete(cls).where(cls.id == id)
        await async_db_session.execute(query)
        await async_db_session.commit()

    @classmethod
    async def all(cls):
        query = select(cls)
        results = (await async_db_session.execute(query)).scalars().all()
        return results


# Imports for alembic autogenerate function
from user.models import User, UserScreener, UserStockNotifier, UserFavoriteStock, UserCode, CodeTargetEnum
from stock.models import Stock
from screener.models import Screener
