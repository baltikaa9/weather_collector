import asyncio
import sys

from utils import init_cities, fetch_weather


async def main():
    options = sys.argv[1:]

    if 'init' in options:
        await init_cities()
    elif 'collect' in options:
        await fetch_weather()


if __name__ == '__main__':
    asyncio.run(main())
