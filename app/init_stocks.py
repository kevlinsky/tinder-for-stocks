import asyncio
import json
import tinvest

from random import randint
from os import environ
from typing import List, Dict

from .crawler import Crawler
from .db import Stock

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

    crawler = Crawler(ALPHAVANTAGE_TOKEN, FINNHUB_TOKEN, ticker_figi_list)
    crawler.run()
    crawler_results = crawler.get_result()

    for alpha_result, finnhub_result in crawler_results:
        if "ERROR" in alpha_result:
            continue
        figi = ''
        for ticker, figi_ in ticker_figi_list:
            if ticker == alpha_result["Symbol"]:
                figi = figi_

        await Stock.create(market_link=f'https://www.tinkoff.ru/invest/stocks/{alpha_result["Symbol"]}',
                           currency=alpha_result["Currency"],
                           market_sector=alpha_result["Sector"],
                           region=alpha_result["Country"],
                           index=alpha_result["Exchange"],
                           market_cap=alpha_result["MarketCapitalization"],
                           ebitda=alpha_result["EBITDA"],
                           debt_equity=finnhub_result["metric"]["totalDebt/totalEquityAnnual"],
                           p_e=alpha_result["PERatio"],
                           roa=alpha_result["ReturnOnAssetsTTM"],
                           roe=alpha_result["ReturnOnEquityTTM"],
                           beta=alpha_result["Beta"],
                           revenue=finnhub_result["freeOperatingCashFlow/revenue5Y"],
                           debt=finnhub_result["totalDebtCagr5Y"],
                           expenses=0,
                           price=0,
                           figi=figi)

    await client.close()


asyncio.run(get_stocks_data())
