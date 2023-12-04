import matplotlib as mp
import numpy as np
from matplotlib import pyplot as plt
import matplotlib as mpl
from scipy.interpolate import make_interp_spline, BSpline

from logic.logic import get_advanced_hourly_forecast, get_day_of_week_capitalized, get_today

INTERPOLATION_COEFFICIENT = 20

mpl.rcParams['axes.labelsize'] = 18
mpl.rcParams['axes.titlesize'] = 20
mpl.rcParams['xtick.labelsize'] = 18
mpl.rcParams['ytick.labelsize'] = 18


def interpolate_line(x, y, k_coeff):
    x_arr = np.array(x).astype(float)
    y_arr = np.array(y).astype(float)

    x_range = np.arange(len(x))

    spline = make_interp_spline(x_range, y_arr, k=k_coeff)

    x_smooth = np.linspace(0, len(x_arr) - 1, INTERPOLATION_COEFFICIENT * x_arr.size)

    y_smooth = spline(x_smooth)

    interpolated_x_in_x = np.interp(x_smooth, x_range, x_arr)

    return interpolated_x_in_x, y_smooth


def graph_temperature(canvas, hours, temperatures, temperatures_feel):

    canvas.plot(hours, temperatures, 'r', label="Temperatura rzeczywista", linewidth=4.0)
    canvas.plot(hours, temperatures_feel, 'b', label="Temperatura odczuwalna", linewidth=4.0)
    canvas.legend(fontsize=14)

    canvas.set_ylabel('Temperatura [°C]')

    canvas.margins(x=0.0)

    canvas.grid(True)


def graph_rainfall(canvas, hours, rainfall, humidity):

    secondary_canvas = canvas.twinx()
    secondary_canvas.plot(hours, humidity, color='#ff9914', linewidth=4.0)
    canvas.bar(hours[:-1], rainfall[:-1], width=0.8, color='#29bf12', edgecolor='#006400', linewidth=4.0, align='edge')
    canvas.set_ylim(bottom=0)

    canvas.margins(x=0.0)

    canvas.set_ylabel('Opady [mm/h]')
    secondary_canvas.set_ylabel('Wilgotność [%]')
    canvas.grid(True)


def graph_wind(canvas, hours, wind_speed, wind_gust):

    canvas.plot(hours, wind_speed, linewidth=3.0, color='#4189e8')
    canvas.hlines(wind_gust, xmin=[i - 0.2 for i, x in enumerate(hours)], xmax=[i + 0.2 for i, x in enumerate(hours)], colors='red', label='Podmuchy wiatru')

    canvas.margins(x=0.0)

    canvas.set_ylabel('Prędkość wiatru [km/h]')

    secondary_canvas = canvas.twinx()
    secondary_canvas.plot(hours, [x * 1000 / 3600 for x in wind_speed], linewidth=3.0, color='#4189e8')
    secondary_canvas.set_ylim(canvas.get_ylim()[0] * 1000 / 3600, canvas.get_ylim()[1] * 1000 / 3600)
    secondary_canvas.set_ylabel('Prędkość wiatru [m/s]')

    canvas.grid(True)


def generate_graphs_image():
    forecast = get_advanced_hourly_forecast()

    figure, axes = plt.subplots(3, 1, figsize=(10, 9))

    hours = forecast['hours']

    axes[0].set_title(f'{get_day_of_week_capitalized()}, {get_today()}')

    graph_temperature(
        axes[0], hours,
        temperatures=forecast['temperature'],
        temperatures_feel=forecast['temperature_feel'])
    graph_rainfall(
        axes[1], hours,
        rainfall=forecast['rainfall'],
        humidity=forecast['humidity'])
    graph_wind(
        axes[2], hours,
        wind_speed=forecast['wind_speed'],
        wind_gust=forecast['wind_gust']
    )

    plt.tight_layout()
    plt.savefig('./assets/generated_images/graphs.png', pil_kwargs={'compress_level': 7})


