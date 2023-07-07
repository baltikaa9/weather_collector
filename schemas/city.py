from pydantic import BaseModel


class City(BaseModel):
    id: int
    name: str
    latitude: float
    longitude: float
    countryCode: str
    population: int
