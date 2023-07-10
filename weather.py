from fake_headers import Headers
import time

from bs4 import BeautifulSoup
import requests

class Weather:
    __weather_link = 'https://world-weather.ru/pogoda/russia/moscow/'

    def __init__(self):
        self.headers = Headers().generate()
        self.data = {period: {'temperature': 'no data', 'pressure': 'no data', 'humidity': 'no data'} for period in ['night', 'morning', 'day', 'evening']}

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

    def collect_data(self):
        try:
            response = self.test_req(self.__weather_link)
        except Exception as e:
            print(f'[ERROR]: exception occurred in {__name__}.py => {e}')
            return

        soup = BeautifulSoup(response.text, 'lxml')

        table = soup.find('div', class_='pane').find('table', class_='weather-today')

        for period in ['night', 'morning', 'day', 'evening']:
            try:
                period_tag = table.find('tr', class_=f'{period}')
                self.data[f'{period}']['temperature'] = period_tag.find('td', class_='weather-temperature').find('span').text.strip()
                self.data[f'{period}']['pressure'] = period_tag.find('td', class_='weather-pressure').text.strip()
                self.data[f'{period}']['humidity'] = period_tag.find('td', class_='weather-humidity').text.strip()
            except Exception as e:
                print(f'[ERROR]: exception occurred in {__name__}.py => {e}')


def main():
    weather = Weather()
    weather.collect_data()
    print(weather.data)


if __name__ == '__main__':
    main()
