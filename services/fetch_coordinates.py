import json

from config import CITIES_FILE
from schemas.coordinates import Coordinates


def fetch_coordinates_from_json() -> list[Coordinates]:
    coordinates: list[Coordinates] = []

    try:
        with open(CITIES_FILE, 'r') as file:
            cities = json.load(file)

        for city in cities:
            coordinates.append(Coordinates.model_validate(city))

        return coordinates
    except FileNotFoundError:
        print('Initialize the cities first: \'python main.py init\'')


if __name__ == '__main__':
    CITIES_FILE = '..\\' + str(CITIES_FILE)
    print(fetch_coordinates_from_json())
