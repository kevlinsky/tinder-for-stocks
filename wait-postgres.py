import asyncio
import asyncpg
import os
from time import sleep


async def run():
    conn_status = False
    while not conn_status:
        try:
            conn = await asyncpg.connect(user=os.environ.get("POSTGRES_USER"),
                                         password=os.environ.get("POSTGRES_PASSWORD"),
                                         database=os.environ.get("POSTGRES_DB"),
                                         host=os.environ.get("POSTGRES_HOST"),
                                         port=os.environ.get("POSTGRES_PORT"))
            conn_status = True
        except (asyncpg.exceptions.PostgresError, ConnectionRefusedError):
            sleep(1)
            continue

        await conn.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(run())
