import asyncio

from stock.recommender import Recommender
from app.mail import send_weekly_digest


async def cron_weekly_digest():
    recommender = Recommender()
    await recommender.fit()
    digest = await recommender.generate_weekly_digest()
    await send_weekly_digest(digest)
    print('Weekly digest sent!')

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(cron_weekly_digest())
