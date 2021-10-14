import asyncio
import json
from time import sleep
from os import getenv

import tinvest
import finnhub

TINVEST_TOKEN = getenv("TINVEST_TOKEN", "t.3YhllsOcci5Vtv-Jb8zTEvHCENfOL73TUXhYuwcjEf76htUdaHA13E_2RHKleJYHJK7VqO2Dhcqmq1W2Nsniew")
FINNHUB_TOKEN = getenv("FINNHUB_TOKEN", "c4tj8hqad3iertukhj80")


async def main():
    client = tinvest.AsyncClient(TINVEST_TOKEN)
    response = await client.get_market_stocks()
    d = json.loads(response.json())["payload"]["instruments"]

    i = 0

    stocks_list = []
    for key in d:
        if i == 100:
            break
        if key["currency"] == "USD":
            stocks_list.append(key["ticker"])
            i += 1

    finnhub_client = finnhub.Client(api_key=FINNHUB_TOKEN)

    res = finnhub_client.company_basic_financials(stocks_list[0], 'all')["metric"]

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


def mem():
    try:
        a = 1 / 0
    except ZeroDivisionError as ex:
        print("нельзя")
        return ex
    return a


print(mem())
