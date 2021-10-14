import logging
import urllib.request
import urllib.error
import json
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed
from time import sleep


class CrawlerAlpha:
    MAX_WORKERS = 5
    CLIENT_TIMEOUT = 30

    __logger = logging.getLogger(__name__)
    __access_handler = logging.FileHandler(filename='./logs/access_api.log', mode='a')
    __error_handler = logging.FileHandler(filename='./logs/error_api.log', mode='a')
    __access_handler.setFormatter(
        logging.Formatter("%(levelname)s: [%(asctime)s] - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
    __error_handler.setFormatter(
        logging.Formatter("%(levelname)s: [%(asctime)s] - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
    __access_handler.setLevel("INFO")
    __error_handler.setLevel("WARNING")
    __logger.addHandler(__access_handler)
    __logger.addHandler(__error_handler)

    def __init__(self, token: str, stocks: List[str], request_limit=5):
        self.token: str = token
        self.stocks: List[str] = stocks
        self.request_limit: int = request_limit
        self.results: List[Dict] = []

    def handling_urls(self, ticker: str) -> Dict:
        url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={self.token}'
        try:
            response = urllib.request.urlopen(url, timeout=CrawlerAlpha.CLIENT_TIMEOUT)
            CrawlerAlpha.__logger.info(f"GET response from API: {url}")
        except (urllib.error.URLError, urllib.error.HTTPError, Exception) as exc:
            CrawlerAlpha.__logger.error(exc, exc_info=True)
            return {"Symbol": ticker, "ERROR": "CHECK LOGS"}
        response_json = response.read().decode('utf-8')
        return json.loads(response_json)

    def run(self):
        limit_list_stocks: List[str] = []
        count_stocks: int = 0
        while self.stocks:
            while self.stocks and count_stocks < self.request_limit:
                limit_list_stocks.append(self.stocks.pop(0))
                count_stocks += 1

            with ThreadPoolExecutor(max_workers=CrawlerAlpha.MAX_WORKERS) as executor:
                futures = {executor.submit(self.handling_urls, ticker): ticker for ticker in limit_list_stocks}

                for future in as_completed(futures):
                    response_json = future.result()
                    self.results.append(response_json)

            count_stocks = 0
            limit_list_stocks.clear()
            sleep(60.5)

    def get_result(self) -> List[Dict]:
        return self.results
