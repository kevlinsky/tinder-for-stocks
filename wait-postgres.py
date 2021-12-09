import asyncio
import asyncpg
from os import environ
from time import sleep

from app.db import User, UserFavoriteStock, UserCode, UserScreener, UserStockNotifier
from app.db import Stock, Screener

from asyncpg.exceptions import UndefinedTableError
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.exc import IntegrityError

from alembic.config import Config
from alembic import command


def startup():
    async def run():
        conn_status = False
        while not conn_status:
            try:
                conn = await asyncpg.connect(user=environ.get("POSTGRES_USER"),
                                             password=environ.get("POSTGRES_PASSWORD"),
                                             database=environ.get("POSTGRES_DB"), host=environ.get("POSTGRES_HOST"),
                                             port=environ.get("POSTGRES_PORT"))
                conn_status = True
            except (asyncpg.exceptions.PostgresError, ConnectionRefusedError):
                sleep(1)
                continue

            await conn.close()

    asyncio.run(run())


def migrations():
    try:
        alembic_cfg = Config("/usr/src/alembic.ini")
        command.upgrade(alembic_cfg, "head")
    except IntegrityError:
        pass

    async def wait_migrations():
        nonlocal alembic_cfg
        migrations_status = False
        while not migrations_status:
            try:
                await User.all()
                await UserFavoriteStock.all()
                await UserCode.all()
                await UserScreener.all()
                await UserStockNotifier.all()
                await Stock.all()
                await Screener.all()
                migrations_status = True
            except (ConnectionRefusedError, UndefinedTableError, ProgrammingError):
                command.upgrade(alembic_cfg, "head")
                sleep(3)
                break

    asyncio.run(wait_migrations())


startup()
migrations()
