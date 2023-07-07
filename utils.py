from config import CITY_COUNT
from services.city_collector import CityCollector
from services.weather_collector import WeatherCollector


async def init_cities():
    city_collector = CityCollector()
    await city_collector.fetch(CITY_COUNT)
    await city_collector.save_to_db()


async def fetch_weather():
    weather_collector = WeatherCollector()
    weather = await weather_collector.fetch()
    await weather_collector.save_to_db()
