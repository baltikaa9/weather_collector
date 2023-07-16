import asyncio
import sys

import flet

from utils import init_cities, fetch_weather
from config import SCHEDULE_TIME
from services.visualizator.GUI import main as visual


async def main():
    options = sys.argv[1:]

    if options[0] == 'init':
        await init_cities()
    elif options[0] == 'collect':
        while True:
            await fetch_weather()
            await asyncio.sleep(SCHEDULE_TIME)
    elif (options[0] == 'visual') & (len(options) == 2):
        if options[1] == '-w':
            await flet.app_async(visual, view=flet.WEB_BROWSER, port=8550)
    elif options[0] == 'visual':
        await flet.app_async(visual)


if __name__ == '__main__':
    asyncio.run(main())
