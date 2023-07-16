import flet as ft
import matplotlib
import matplotlib.pyplot as plt
from flet.matplotlib_chart import MatplotlibChart

from services.visualizator.chart import Chart
from services.visualizator.helper import get_cities, get_weathers

matplotlib.use('svg')


async def main(page: ft.Page):
    city_dict = await get_cities()
    fig, ax = plt.subplots()

    chart = Chart(fig, ax)

    async def visualization(e):
        if flet_chart in page.controls:
            await page.remove_async(flet_chart)
        city_name = city_list.value
        weathers = await get_weathers(city_dict[city_name])
        chart.draw(weathers.keys(), weathers.values(), city_name, color='white', marker='o')
        await page.add_async(flet_chart)

    city_list = ft.Dropdown(label='City',
                            hint_text='Choose city',
                            options=[
                                ft.dropdown.Option(city_name) for city_name in city_dict.keys()
                            ],
                            on_change=visualization
                            )

    flet_chart = MatplotlibChart(fig, expand=True, transparent=True)

    await page.add_async(
        city_list,
    )


if __name__ == '__main__':
    ft.app(target=main, view=ft.WEB_BROWSER, port=8550)
