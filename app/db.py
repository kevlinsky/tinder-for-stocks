import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.models import Base

host = os.getenv('POSTGRES_HOST')
db = os.getenv('POSTGRES_DB')
port = os.getenv('POSTGRES_PORT')
user = os.getenv('POSTGRES_USER')
password = os.getenv('POSTGRES_PASSWORD')

SQLALCHEMY_DATABASE_URL = f'postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}'

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
