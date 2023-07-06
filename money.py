import requests
from bs4 import BeautifulSoup
import time


class Currency:
    """Collects currencies form website"""

    currency_link = 'https://ru.investing.com/'
    currencies_links = {
        'USD/RUB': 'currencies/usd-rub/',
        'EUR/RUB': 'currencies/eur-rub/',
        'BTC/USD': 'crypto/bitcoin/',
    }

    headers = {
        'Age': '74196',
        'Alt-Svc': 'h3=":443"; ma=86400',
        'Cache-Control': 'public, max-age=581383',
        'Cf-Cache-Status': 'HIT',
        'Cf-Ray': '7e1f69cbcd07b351-PRG',
        'Content-Encoding:': 'br',
    }

    def __init__(self):
        self.currencies_prices = {}

    def set_currency(self):
        """Knows currency prices from the web"""

        for curr, link in self.currencies_links.items():
            try:
                page = requests.get(self.currency_link + link)
                soup = BeautifulSoup(page.content, 'lxml')

                if 'currencies' in link:
                    convert = soup.select(
                        'div.instrument-price_instrument-price__xfgbB span.text-2xl[data-test="instrument-price-last"]'
                    )
                elif 'crypto' in link:
                    convert = soup.select(
                        'div.cryptoCurrentData div.top span.inlineblock span#last_last'
                    )

                self.currencies_prices[curr] = convert[0].text.replace('.', '')

            except:
                print(f'#Exception occured with {curr}')
            # else:
            #     print(f'#Succeed with {curr}')
            finally:
                time.sleep(1)

    def get_currency(self) -> dict:
        """Gets currency prices"""

        return self.currencies_prices


def main():
    currency = Currency()
    currency.set_currency()
    prices = currency.get_currency()
    print(prices)


if __name__ == '__main__':
    main()
