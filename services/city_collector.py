import requests
import json

from database.dals import CityDAL
from exceptions import ApiServiceError
from schemas.base import BaseSchema
from schemas.city import City
from config import OXILOR_API_KEY, CITIES_FILE
from database.session import async_session
from services.base import BaseCollector


class CityCollector(BaseCollector):
    def __init__(self):
        super().__init__()

    async def fetch(self, count: int = 50) -> list[BaseSchema]:
        f"""Fetch {count} cities from API"""
        url = f'https://data-api.oxilor.com/rest/regions?type=city&first={count}'
        headers = {
            'Authorization': f'Bearer {OXILOR_API_KEY}'
        }

        response = requests.get(url, headers=headers)
        try:
            cities = response.json()['edges']
            for city in cities:
                self.storage.append(City.model_validate(city['node']))
        except KeyError:
            raise ApiServiceError
        else:
            print('[INFO] Fetch cities successful.')
            return self.storage

    async def save_to_db(self) -> None:
        """Write the list of cities to the DB"""
        async with async_session() as session:
            city_dal = CityDAL(session)

            await city_dal.truncate_table()

            for city in self.storage:
                await city_dal.add_city(city)

            await city_dal.save_datetime()

        print('[INFO] Save cities to db successful.')


    def save_to_json(self) -> None:
        cities_json = [json.loads(city.model_dump_json()) for city in self.storage]
        with open(CITIES_FILE, 'w', encoding='utf-8') as file:
            json.dump(cities_json, file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    CITIES_FILE = '..\\' + str(CITIES_FILE)

    collector = CityCollector()

    collector.fetch()
    collector.save_to_json()
