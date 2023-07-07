from config import CITY_COUNT
from services.city_collector import CityCollector
from services.weather_collector import WeatherCollector


async def init_cities():
    city_collector = CityCollector()
    city_collector.fetch_cities(CITY_COUNT)
    # city_collector.save_cities_to_json()
    await city_collector.save_cities_to_db()


async def fetch_weather():
    weather_collector = WeatherCollector()
    weather = await weather_collector.fetch_weather()
    await weather_collector.save_weathers_in_db()
