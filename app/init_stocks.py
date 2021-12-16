import asyncio
import json
import os

import tinvest

from random import randint
from typing import List, Dict

from stock.models import Stock
from app.crawler import Crawler

TINVEST_TOKEN = os.environ.get("TINVEST_TOKEN")
FINNHUB_TOKEN = os.environ.get("FINNHUB_TOKEN")
ALPHAVANTAGE_TOKEN = os.environ.get("ALPHAVANTAGE_TOKEN")


def to_numeric(data):
    if not data or data == "None":
        return "0"
    return data


async def get_stocks_data(count_of_stocks: int = 5):
    client = tinvest.AsyncClient(TINVEST_TOKEN)
    response = await client.get_market_stocks()
    response_instruments: List[Dict] = json.loads(response.json())["payload"]["instruments"]
    await client.close()

    ticker_figi_list: List[List[str, str]] = []

    while len(ticker_figi_list) < count_of_stocks:
        num = randint(0, 1000)
        instrument = response_instruments[num]
        if instrument["currency"] == "USD":
            l = [instrument["ticker"], instrument["figi"]]
            if l not in ticker_figi_list:
                ticker_figi_list.append(l)

    crawler = Crawler(ALPHAVANTAGE_TOKEN, FINNHUB_TOKEN, ticker_figi_list)
    crawler.run()
    crawler_results = crawler.get_result()

    for alpha_result, finnhub_result, price_result in crawler_results:
        if "ERROR" in alpha_result:
            continue

        figi = ''
        for ticker, figi_ in ticker_figi_list:
            if ticker == alpha_result['Symbol']:
                figi = figi_

        await Stock.create(market_link=f'https://www.tinkoff.ru/invest/stocks/{alpha_result["Symbol"]}',
                           currency=alpha_result["Currency"],
                           market_sector=alpha_result["Sector"],
                           region=alpha_result["Country"],
                           exchange=alpha_result["Exchange"],
                           market_cap=to_numeric(alpha_result.get("MarketCapitalization", 0)),
                           ebitda=to_numeric(alpha_result.get("EBITDA", 0)),
                           debt_equity=to_numeric(finnhub_result.get("totalDebt/totalEquityAnnual", 0)),
                           p_e=to_numeric(alpha_result.get("PERatio", 0)),
                           roa=to_numeric(alpha_result.get("ReturnOnAssetsTTM", 0)),
                           roe=to_numeric(alpha_result.get("ReturnOnEquityTTM", 0)),
                           beta=to_numeric(alpha_result.get("Beta", 0)),
                           revenue=to_numeric(finnhub_result.get("freeOperatingCashFlow/revenue5Y", 0)),
                           debt=to_numeric(finnhub_result.get("totalDebtCagr5Y", 0)),
                           price=to_numeric(price_result.get('c', 0)),
                           figi=figi)


if __name__ == '__main__':
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(get_stocks_data(count_of_stocks=5))
