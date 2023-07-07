import datetime

from sqlalchemy import text, select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import CityDB, CityCreatedAt, WeatherDB
from schemas.city import City
from schemas.weather import Weather


class CityDAL:
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def truncate_table(self):
        await self.__session.execute(text('TRUNCATE TABLE cities RESTART IDENTITY CASCADE;'))

    async def add_city(self, city: City) -> CityDB:
        new_city = CityDB(
            id=city.id,
            name=city.name,
            latitude=city.latitude,
            longitude=city.longitude,
            country=city.countryCode,
            population=city.population
        )

        self.__session.add(new_city)
        await self.__session.commit()
        return new_city

    async def save_datetime(self) -> CityCreatedAt:
        created_at = CityCreatedAt(created_at=datetime.datetime.now())
        self.__session.add(created_at)
        await self.__session.commit()
        return created_at

    async def get_city_by_coords(self, latitude: float, longitude: float) -> CityDB:
        query = select(CityDB).where((City.latitude == latitude) & (City.longitude == longitude))
        city = await self.__session.execute(query)
        city = city.fetchone()
        if city:
            return city[0]

    async def get_all_cities(self) -> list[CityDB]:
        query = select(CityDB)
        cities = await self.__session.execute(query)
        cities = cities.all()
        cities = [city[0] for city in cities]
        return cities


class WeatherDAL:
    def __init__(self, session):
        self.__session = session

    async def add_weather(self, weather: Weather):
        new_weather = WeatherDB(
            city_id=weather.city_id,
            type=weather.type,
            temperature=weather.main.temperature,
            pressure=weather.main.pressure,
            humidity=weather.main.humidity,
            wind_speed=weather.wind.speed,
            wind_deg=weather.wind.deg,
            cloudiness=weather.cloudiness,
            created_at=datetime.datetime.now()
        )
        self.__session.add(new_weather)
        await self.__session.commit()
        return new_weather
