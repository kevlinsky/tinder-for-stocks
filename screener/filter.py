from screener.models import Screener
from stock.models import Stock
from app.db import async_db_session
from sqlalchemy import select


async def filter_stocks(screener: Screener):
    screener_str_fields = ['currency', 'market_sector', 'region', 'index']

    screener_str_dct = {}
    for name in screener_str_fields:
        value = getattr(screener, name)
        if value:
            screener_str_dct[name] = value.split(', ')

    screener_num_fields = ['market_cap', 'ebitda', 'debt_equity', 'p_e', 'roa',
                           'roe', 'beta', 'revenue', 'debt', 'price']

    screener_num_dct = {}
    for name in screener_num_fields:
        value = getattr(screener, name)
        if value:
            screener_num_dct[name] = value.split(' - ')

    conditions_str = [getattr(Stock, attr_name).in_(value) for attr_name, value in screener_str_dct.items()]
    conditions_num = []
    for attr_name, value in screener_num_dct.items():
        fr = float(value[0])
        to = float(value[1])
        cond1 = getattr(Stock, attr_name) > fr
        conditions_num.append(cond1)
        cond2 = getattr(Stock, attr_name) < to
        conditions_num.append(cond2)

    conditions = [*conditions_str, *conditions_num]
    query = select(Stock).filter(*conditions)

    results = (await async_db_session.execute(query)).scalars().all()
    return results
