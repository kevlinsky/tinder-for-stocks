import asyncio
import json
import tinvest

from random import randint
from time import sleep
from os import environ
from typing import List, Dict

TINVEST_TOKEN = environ.get("TINVEST_TOKEN")
FINNHUB_TOKEN = environ.get("FINNHUB_TOKEN")
ALPHAVANTAGE_TOKEN = environ.get("ALPHAVANTAGE_TOKEN")


async def get_stocks_data():
    client = tinvest.AsyncClient(TINVEST_TOKEN)
    response = await client.get_market_stocks()
    response_instruments: List[Dict] = json.loads(response.json())["payload"]["instruments"]

    ticker_figi_list: List[List[str, str]] = []
    cnt = 0
    for instrument in response_instruments:
        if cnt == 30:
            break
        num = randint(0, 1800)
        if instrument[num]["currency"] == "USD":
            ticker_figi_list.append([instrument["ticker"], instrument["figi"]])
            cnt += 1


    """
    market_link = generate link from tinkoff
    currency = from tinvest
    market_sector = Sector
    region = Country
    index = Exchange
    market_cap = MarketCapitalization
    ebitda = EBITDA
    debt_equity = totalDebt/totalEquityAnnual
    p_e = PERatio
    roa = ReturnOnAssetsTTM
    roe = ReturnOnEquityTTM
    beta = Beta
    revenue = freeOperatingCashFlow/revenue5Y
    debt = totalDebtCagr5Y
    expenses = ?
    price = from tinvest
    figi = from tinvest
    """
    await client.close()
