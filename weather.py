from bs4 import BeautifulSoup
import requests
from fake_headers import Headers


class Weather:
    __weather_link = 'https://www.accuweather.com/en/ru/moscow/294021/weather-forecast/294021/'

    def __init__(self):
        self.__data = []

    def set_weather(self):
        try:
            page = requests.get(self.__weather_link, headers=Headers().generate())
            soup = BeautifulSoup(page.content, 'lxml')
            print(page.content[:500])
            temperature = soup.select_one('a.cur-con-weather-card div.forecast-container div.temp').text
            phrase = soup.select_one('a.cur-con-weather-card card-module div.spaced-content span.phrase').text
            self.__data += [temperature, phrase]

        except Exception as e:
            print(f'Exception occurred in getting weather -> {e}')

    def get_weather(self) -> list[str]:
        return self.__data


def main():
    weather = Weather()
    weather.set_weather()
    print(weather.get_weather())


if __name__ == '__main__':
    main()
