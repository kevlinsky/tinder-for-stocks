import asyncio

from stock.recommender import Recommender
from app.mail import send_monthly_digest


async def cron_monthly_digest():
    recommender = Recommender()
    await recommender.fit()
    digest = await recommender.generate_monthly_digest()
    await send_monthly_digest(digest)
    print('Monthly digest sent!')

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(cron_monthly_digest())
