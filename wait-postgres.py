import asyncio
import asyncpg
from os import getenv
from time import sleep


async def run():
    conn_status = False
    while not conn_status:
        try:
            conn = await asyncpg.connect(user=getenv("POSTGRES_USER"), password=getenv("POSTGRES_PASSWORD"),
                                         database=getenv("POSTGRES_DB"), host=getenv("POSTGRES_HOST"))
            conn_status = True
        except asyncpg.exceptions.PostgresError:
            sleep(1)
            continue

        await conn.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(run())
