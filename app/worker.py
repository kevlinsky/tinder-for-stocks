import json
import os
import asyncio
import logging

import tinvest
import aiopg
from tinvest.exceptions import UnexpectedError
from celery import Celery
from celery.utils.log import get_task_logger

from app.mail import send_confirmation_email, send_password_reset_email
from app.init_stocks import TINVEST_TOKEN

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get('CELERY_BROKER_URL')
celery.conf.result_backend = os.environ.get('CELERY_RESULT_BACKEND')

logger = get_task_logger(__name__)
logger_handler = logging.FileHandler('./logs/celery.log')
logger_handler.setFormatter(
    logging.Formatter("%(levelname)s: [%(asctime)s] - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
logger.addHandler(logger_handler)


@celery.task(name='confirmation_email')
def confirmation_email(email_to: str, hash: str):
    asyncio.get_event_loop().run_until_complete(send_confirmation_email(email_to, hash))
    logger.info(f"confirmation email to {email_to} has been sent")
    return {'message': f'Confirmation email to {email_to} has been sent'}


@celery.task(name='password_reset')
def password_reset(email_to: str, code: int):
    asyncio.get_event_loop().run_until_complete(send_password_reset_email(email_to, code))
    logger.info(f"password reset to {email_to} has been sent")
    return {'message': f'Password reset email to {email_to} has been sent'}


@celery.task(name='stocks_update')
def stocks_update():
    async def retrieve():
        conn = await aiopg.connect(database=os.getenv('POSTGRES_DB'), host=os.getenv('POSTGRES_HOST'),
                                   user=os.getenv('POSTGRES_USER'), password=os.getenv('POSTGRES_PASSWORD'),
                                   port=os.getenv('POSTGRES_PORT'))
        cursor = await conn.cursor()

        client = tinvest.AsyncClient(TINVEST_TOKEN)
        await cursor.execute("SELECT figi FROM stocks;")
        stocks = await cursor.fetchall()

        for figi in stocks:
            try:
                response = await client.get_market_orderbook(figi, 20)
            except UnexpectedError:
                await client.close()
                logger.error("LIMIT OF TINVEST IS OUT!")
                break
            last_price = json.loads(response.json())["payload"]["last_price"]
            await cursor.execute("BEGIN;")
            await cursor.execute("UPDATE stocks SET price = (%s) WHERE figi = (%s);", (last_price, figi))
            await cursor.execute("COMMIT;")

        await client.close()

    asyncio.run(retrieve())


celery.add_periodic_task(60.0, stocks_update.s(), name='add-every-minute-update-stocks')
