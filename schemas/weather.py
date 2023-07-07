from dataclasses import dataclass
from enum import Enum

from pydantic import BaseModel, Field

from schemas.base import BaseSchema


class WeatherType(str, Enum):
    THUNDERSTORM = 'Гроза'
    DRIZZLE = 'Изморось'
    RAIN = 'Дождь'
    SNOW = 'Снег'
    CLEAR = 'Ясно'
    MIST = 'Туман'
    CLOUDS = 'Облачно'


class WeatherMain(BaseModel):
    temperature: float = Field(alias='temp')
    pressure: float
    humidity: int


class WeatherWind(BaseModel):
    speed: float
    deg: int


@dataclass
class Weather(BaseSchema):
    city_id: int
    type: WeatherType
    main: WeatherMain
    wind: WeatherWind
    cloudiness: int
