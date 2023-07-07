import requests
import json

from database.dals import CityDAL
from exceptions import ApiServiceError
from schemas.city import City
from config import OXILOR_API_KEY, CITIES_FILE
from database.session import async_session


class CityCollector:
    def __init__(self):
        self.__cities: list[City] = []

    def fetch_cities(self, count: int = 50) -> list[City]:
        url = f'https://data-api.oxilor.com/rest/regions?type=city&first={count}'

        headers = {
            'Authorization': f'Bearer {OXILOR_API_KEY}'
        }

        response = requests.get(url, headers=headers)
        try:
            cities = response.json()['edges']
            for city in cities:
                self.__cities.append(City.model_validate(city['node']))

            return self.__cities
        except KeyError:
            raise ApiServiceError

    async def save_cities_to_db(self) -> None:
        async with async_session() as session:
            city_dal = CityDAL(session)

            await city_dal.truncate_table()

            for city in self.__cities:
                await city_dal.add_city(city)

            await city_dal.save_datetime()

    def save_cities_to_json(self) -> None:
        cities_json = [json.loads(city.model_dump_json()) for city in self.__cities]
        with open(CITIES_FILE, 'w', encoding='utf-8') as file:
            json.dump(cities_json, file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    CITIES_FILE = '..\\' + str(CITIES_FILE)

    collector = CityCollector()

    collector.fetch_cities()
    collector.save_cities_to_json()
