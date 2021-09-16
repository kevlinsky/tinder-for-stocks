from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from models import Base
import os

host = os.environ.get('DB_HOST')
name = os.environ.get('DB_NAME')
port = os.environ.get('DB_PORT')
user = os.environ.get('DB_USER')
password = os.environ.get('DB_USER_PASSWORD')

SQLALCHEMY_DATABASE_URL = f'postgresql+asyncpg://{user}:{password}@{host}:{port}/{name}'

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)


async def init_db():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
