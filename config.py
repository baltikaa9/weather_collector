import os
import pathlib

from dotenv import load_dotenv

load_dotenv()

OXILOR_API_KEY = os.getenv('OXILOR_API_KEY')
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')

CITIES_FILE = pathlib.Path('data', 'cities.json')

CITY_COUNT = 50

DB_URL = os.getenv('DB_URL')

DB_ECHO = False

if __name__ == '__main__':
    print(CITIES_FILE)


