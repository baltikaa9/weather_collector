import asyncio
import sys

from utils import init_cities, fetch_weather
from config import SCHEDULE_TIME


async def main():
    options = sys.argv[1:]

    if 'init' in options:
        await init_cities()
    elif 'collect' in options:
        while True:
            await fetch_weather()
            await asyncio.sleep(SCHEDULE_TIME)


if __name__ == '__main__':
    asyncio.run(main())
