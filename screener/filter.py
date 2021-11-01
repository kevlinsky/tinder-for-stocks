from sqlalchemy import select
from screener.models import Screener
from stock.models import Stock
from app.db import async_db_session


async def filter_stocks(screener: Screener):
    currency = screener.currency.split(', ')
    market_sectors = screener.market_sector.split(', ')
    regions = screener.region.split(', ')
    indexes = screener.index.split(', ')
    market_cap = screener.market_cap.split(' ')
    ebitda = screener.ebitda.split(' ')
    debt_equity = screener.debt_equity.split(' ')
    p_e = screener.p_e.split(' ')
    roa = screener.roa.split(' ')
    roe = screener.roe.split(' ')
    beta = screener.beta.split(' ')
    revenue = screener.revenue.split(' ')
    debt = screener.debt.split(' ')
    price = screener.price.split(' ')

    if currency == ['']:
        currency = ['USD']

    if market_sectors == ['']:
        market_sectors = ['FINANCE', 'TECHNOLOGY', 'TRADE & SERVICES',
                          'MANUFACTURING', 'LIFE SCIENCES', 'ENERGY & TRANSPORTATION',
                          'REAL ESTATE & CONSTRUCTION']

    if regions == ['']:
        regions = ['USA']

    if indexes == ['']:
        indexes = ['NYSE', 'NASDAQ']

    if market_cap == ['']:
        market_cap = ['0', '', '5000000000000']

    if ebitda == ['']:
        ebitda = ['-10000000000', '', '200000000000']

    if debt_equity == ['']:
        debt_equity = ['0', '', '30000']

    if p_e == ['']:
        p_e = ['0', '', '20000']

    if roa == ['']:
        roa = ['-1000', '', '200']

    if roe == ['']:
        roe = ['-5000', '', '5000']

    if beta == ['']:
        beta = ['-10', '', '10']

    if revenue == ['']:
        revenue = ['-1000', '', '1000']

    if debt == ['']:
        debt = ['-1000', '', '1000']

    if price == ['']:
        price = ['-1', '', '500000']

    query = select(Stock).filter(Stock.currency.in_(currency),
                                 Stock.market_sector.in_(market_sectors),
                                 Stock.region.in_(regions),
                                 Stock.index.in_(indexes),
                                 Stock.market_cap > float(market_cap[0]), Stock.market_cap < float(market_cap[2]),
                                 Stock.ebitda > float(ebitda[0]), Stock.ebitda < float(ebitda[2]),
                                 Stock.debt_equity > float(debt_equity[0]), Stock.debt_equity < float(debt_equity[2]),
                                 Stock.p_e > float(p_e[0]), Stock.p_e < float(p_e[2]),
                                 Stock.roa > float(roa[0]), Stock.roa < float(roa[2]),
                                 Stock.roe > float(roe[0]), Stock.roe < float(roe[2]),
                                 Stock.beta > float(beta[0]), Stock.beta < float(beta[2]),
                                 Stock.revenue > float(revenue[0]), Stock.revenue < float(revenue[2]),
                                 Stock.debt > float(debt[0]), Stock.debt < float(debt[2]),
                                 Stock.price > float(price[0]), Stock.price < float(price[2]),
                                 )

    results = (await async_db_session.execute(query)).scalars().all()

    return results








