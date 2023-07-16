import asyncio
import datetime

from aiohttp import ClientSession

from config import OPENWEATHER_API_KEY
from database.dals import CityDAL, WeatherDAL
from database.models import CityDB
from database.session import async_session
from exceptions import ApiServiceError
from schemas.base import BaseSchema
from schemas.weather import Weather, WeatherType, WeatherMain, WeatherWind
from services.collector.base import BaseCollector


class WeatherCollector(BaseCollector):
    def __init__(self):
        super().__init__()
        self.tasks_for_asyncio_gather = []

    async def fetch(self) -> list[BaseSchema]:
        """Get all cities from DB and fetch weather for each"""
        cities = await self._get_cities_from_db()
        async with ClientSession() as session:
            for city in cities:
                task = asyncio.create_task(self._fetch_weather_in_city(session, city))

                self.tasks_for_asyncio_gather.append(task)

            await asyncio.gather(*self.tasks_for_asyncio_gather)
        print(f'[INFO] Weather info collected at {datetime.datetime.now()}.')
        return self.storage

    async def _fetch_weather_in_city(self, session: ClientSession, city: CityDB):
        url = f'https://api.openweathermap.org/data/2.5/weather?lat={city.latitude}&lon={city.longitude}&units=metric' \
              f'&appid={OPENWEATHER_API_KEY}'

        response = await session.get(url)
        response_json = await response.json()

        weather = self._parse_weather(response_json, city)
        self.storage.append(weather)

    async def save_to_db(self) -> None:
        """Write list of weather forecasts for each of cities to the DB"""
        async with async_session() as session:
            weather_dal = WeatherDAL(session)

            for weather in self.storage:
                await weather_dal.add_weather(weather)
        print('[INFO] Save weathers to db successful.')

    @staticmethod
    def _parse_weather(response_json: dict, city: CityDB) -> Weather:
        parser = WeatherParser(response_json)

        weather_type = parser.parse_weather_type()
        weather_main = parser.parse_weather_main()
        weather_wind = parser.parse_weather_wind()
        cloudiness = parser.parse_cloudiness()

        weather = {
            'city_id': city.id,
            'type': weather_type,
            'main': weather_main,
            'wind': weather_wind,
            'cloudiness': cloudiness
        }
        return Weather.model_validate(weather)

    @staticmethod
    async def _get_cities_from_db() -> list[CityDB]:
        async with async_session() as session:
            city_dal = CityDAL(session)
            cities = await city_dal.get_all_cities()
        return cities


class WeatherParser:
    def __init__(self, response_json: dict):
        self.response = response_json

    def parse_weather_type(self) -> WeatherType:
        try:
            weather_type_id = str(self.response['weather'][0]['id'])
        except (IndexError, KeyError):
            raise ApiServiceError

        weather_types = {
            '2': WeatherType.THUNDERSTORM,
            '3': WeatherType.DRIZZLE,
            '5': WeatherType.RAIN,
            '6': WeatherType.SNOW,
            '7': WeatherType.MIST,
            '800': WeatherType.CLEAR,
            '80': WeatherType.CLOUDS
        }

        for _id, _weather_type in weather_types.items():
            if weather_type_id.startswith(_id):
                return _weather_type
        raise ApiServiceError

    def parse_weather_main(self) -> WeatherMain:
        try:
            weather_main = WeatherMain.model_validate(self.response['main'])
            return weather_main
        except KeyError:
            raise ApiServiceError

    def parse_weather_wind(self) -> WeatherWind:
        try:
            weather_wind = WeatherWind.model_validate(self.response['wind'])
            return weather_wind
        except KeyError:
            raise ApiServiceError

    def parse_cloudiness(self) -> int:
        try:
            cloudiness = self.response['clouds']['all']
            return cloudiness
        except KeyError:
            raise ApiServiceError


if __name__ == '__main__':
    collector = WeatherCollector()

    print(collector.fetch())
