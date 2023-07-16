import asyncio
import sys

import flet

from utils import init_cities, fetch_weather
from config import SCHEDULE_TIME
from services.visualizator.GUI import main as visual


async def main():
    options = sys.argv[1:]

    if 'init' in options:
        await init_cities()
    elif 'collect' in options:
        while True:
            await fetch_weather()
            await asyncio.sleep(SCHEDULE_TIME)
    elif 'visual' in options:
        await flet.app_async(visual)


if __name__ == '__main__':
    asyncio.run(main())
