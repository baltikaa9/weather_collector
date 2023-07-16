import time

from sqlalchemy.exc import ProgrammingError

from config import CITY_COUNT
from services.collector.city_collector import CityCollector
from services.collector.weather_collector import WeatherCollector


async def init_cities():
    city_collector = CityCollector()
    await city_collector.fetch(CITY_COUNT)
    for _ in range(5):
        try:
            await city_collector.save_to_db()
            break
        except ProgrammingError:
            time.sleep(1)


async def fetch_weather():
    weather_collector = WeatherCollector()
    await weather_collector.fetch()
    for _ in range(5):
        try:
            await weather_collector.save_to_db()
            break
        except ProgrammingError:
            time.sleep(1)
