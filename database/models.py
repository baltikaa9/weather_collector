import datetime
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    ...


class CityCreatedAt(Base):
    __tablename__ = 'cities_created_at'

    created_at: Mapped[datetime.datetime] = mapped_column(primary_key=True)


class CityDB(Base):
    __tablename__ = 'cities'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    latitude: Mapped[float]
    longitude: Mapped[float]
    country: Mapped[str]
    population: Mapped[int]
    weather: Mapped[List['WeatherDB']] = relationship()


class WeatherDB(Base):
    __tablename__ = 'weathers'

    id: Mapped[int] = mapped_column(primary_key=True)
    city_id: Mapped[int] = mapped_column(ForeignKey('cities.id'))
    type: Mapped[str]
    temperature: Mapped[float]
    pressure: Mapped[float]
    humidity: Mapped[int]
    wind_speed: Mapped[float]
    wind_deg: Mapped[int]
    cloudiness: Mapped[int]
    created_at: Mapped[datetime.datetime]

