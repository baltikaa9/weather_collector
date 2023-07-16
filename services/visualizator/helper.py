from database.dals import CityDAL, WeatherDAL
from database.session import async_session


async def get_cities() -> dict:
    async with async_session() as session:
        city_dal = CityDAL(session)
        cities = await city_dal.get_all_cities()
    return {city.name: city.id for city in cities}


async def get_weathers(city_id: int) -> dict:
    async with async_session() as weather_session:
        weather_dal = WeatherDAL(weather_session)
        weathers = await weather_dal.get_weather_by_city_id(city_id)
    return {weather.created_at.strftime('%d-%m-%Y %H:%M'): weather.temperature for weather in weathers}