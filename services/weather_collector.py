import time

import requests

from config import OPENWEATHER_API_KEY
from database.dals import CityDAL, WeatherDAL
from database.session import async_session
from exceptions import ApiServiceError
from schemas.base import BaseSchema
from schemas.weather import Weather, WeatherType, WeatherMain, WeatherWind
from services.base import BaseCollector


class WeatherCollector(BaseCollector):
    def __init__(self):
        super().__init__()

    async def fetch(self) -> list[BaseSchema]:
        cities = await self._get_cities_from_db()
        for city in cities:
            # TODO: вынести url-ы отдельно
            url = f'https://api.openweathermap.org/data/2.5/weather?lat={city.latitude}&lon={city.longitude}&units=metric' \
                  f'&appid={OPENWEATHER_API_KEY}'

            response = requests.get(url)
            response_json = response.json()

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

            self.storage.append(Weather.model_validate(weather))

            print(f'[INFO] Info collected for {len(self.storage)} city.')
            time.sleep(0.1)
        return self.storage

    async def save_to_db(self) -> None:
        async with async_session() as session:
            weather_dal = WeatherDAL(session)

            for weather in self.storage:
                await weather_dal.add_weather(weather)

    @staticmethod
    async def _get_cities_from_db():
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
