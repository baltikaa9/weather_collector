from schemas.base import BaseSchema


class City(BaseSchema):
    id: int
    name: str
    latitude: float
    longitude: float
    countryCode: str
    population: int
