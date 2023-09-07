from fake_headers import Headers
import time

import requests
from bs4 import BeautifulSoup
import time


class Currency:
    """Collects currencies form website"""

    __currency_link = 'https://ru.investing.com/'
    __currencies_links = {
        'USD/RUB': 'currencies/usd-rub/',
        'EUR/RUB': 'currencies/eur-rub/',
        'BTC/USD': 'crypto/bitcoin/',
    }

    def __init__(self):
        self.headers = Headers().generate()
        self.currencies_prices = {}

    def test_req(self, url, tries=5):
        """Wrapper function on requests not to crash code"""
        try:
            response = requests.get(url, headers=self.headers)
            print(f'[+] {url} {response.status_code}')
        except Exception as e:
            time.sleep(3)
            if not tries:
                raise e
            print(f'[INFO] tries={tries} => {url}')
            return self.test_req(url, tries=tries-1)
        else:
            return response

    def collect_currency(self):
        """Knows currency prices from the web"""

        for curr, link in self.__currencies_links.items():
            try:
                response = self.test_req(self.__currency_link + link)
                soup = BeautifulSoup(response.text, 'lxml')
                value = 0

                if 'currencies' in link:
                    value = soup.select_one(
                        'div[data-test="instrument-header-details"] span.text-2xl'
                    ).text.strip()
                elif 'crypto' in link:
                    value = soup.select_one(
                        'div.text-5xl'
                    ).text.strip()

                self.currencies_prices[curr] = value

            except Exception as e:
                print(f'[ERROR]: exception occurred in {__name__}.py => {e}')


def main():
    currency = Currency()
    currency.collect_currency()
    prices = currency.currencies_prices
    print(prices)


if __name__ == '__main__':
    main()
