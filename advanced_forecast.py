import matplotlib as mp
import numpy as np
from matplotlib import pyplot as plt
import matplotlib as mpl
from scipy.interpolate import make_interp_spline, BSpline

INTERPOLATION_COEFFICIENT = 20

mpl.rcParams['axes.labelsize'] = 18
mpl.rcParams['axes.titlesize'] = 20
mpl.rcParams['xtick.labelsize'] = 18
mpl.rcParams['ytick.labelsize'] = 18


def interpolate_line(x, y, k_coeff):
    x_arr = np.array(x).astype(float)
    y_arr = np.array(y).astype(float)

    new_x = np.linspace(x_arr.min(), x_arr.max(), INTERPOLATION_COEFFICIENT * x_arr.size)

    spline = make_interp_spline(x_arr, y_arr, k=k_coeff)
    y_smooth = spline(new_x)

    return new_x, y_smooth


def graph_temperature(canvas, hours):
    temperatures = [-4.5, -2., 0., 5., 2., 1., -0.3, 1.7, 1.9, 6.9, 7.8, 3.0]
    temperatures_felt = [-5.3, -3.2, -1.0, 2.0, 1.0, -0.8, 1.3, -1.5, 0.1, 4.2, 5.0, 3.8]

    _, temperatures_interp = interpolate_line(hours, temperatures, 3)
    hours_extended, temperatures_felt_interp = interpolate_line(hours, temperatures_felt, 3)

    canvas.plot(hours_extended, temperatures_interp, 'r', label="Temperatura rzeczywista", linewidth=4.0)
    canvas.plot(hours_extended, temperatures_felt_interp, 'b', label="Temperatura odczuwalna", linewidth=4.0)
    canvas.plot(np.array(hours).astype(float), temperatures, 'r.', markersize=15)
    canvas.plot(np.array(hours).astype(float), temperatures_felt, 'b.', markersize=15)
    canvas.legend(fontsize=14)

    canvas.set_title('Poniedziałek, 24.06')
    canvas.set_ylabel('Temperatura [°C]')

    canvas.set_xlim(float(hours[0]), float(hours[-1]))

    canvas.grid(True)


def graph_rainfall(canvas, hours):

    rainfall = [11, 12, 10, 15, 20, 10, 7, 0, 1, 3, 3, 6]
    humidity = [0, 0, 0, 0, 15, 20, 32, 11, 8, 4, 0, 1]

    hours_interp, humidity_interp = interpolate_line(np.array(hours).astype(float), np.array(humidity).astype(float), 3)

    secondary_canvas = canvas.twinx()
    secondary_canvas.plot(hours_interp, humidity_interp, color='#ff9914', linewidth=4.0)
    canvas.bar(np.array(hours).astype(float), rainfall, width=0.7, color='#29bf12', edgecolor='#006400', linewidth=2.0)

    canvas.set_xlim(float(hours[0]), float(hours[-1]))

    canvas.set_ylabel('Opady [mm/h]')
    secondary_canvas.set_ylabel('Wilgotność [%]')
    canvas.grid(True)


def graph_wind(canvas, hours):

    wind_speed = [0, 5, 6, 18, 3, 20, 25, 41, 20, 11, 6, 2]
    wind_gust = [5, 11, 21, 28, 27, 29, 45, 47, 26, 17, 10, 5]

    hours_interp, wind_interp = interpolate_line(hours, wind_speed, 3)

    canvas.plot(hours_interp, wind_interp, linewidth=3.0, color='#4189e8')
    canvas.plot(np.array(hours).astype(float), wind_speed, '.', markersize=15, color='#4189e8')
    canvas.errorbar(np.array(hours).astype(float), wind_gust, xerr=0.45, fmt='none', color='#ed3a37')

    canvas.set_xlim(float(hours[0]), float(hours[-1]))

    canvas.set_ylabel('Prędkość wiatru [km/h]')

    secondary_canvas = canvas.twinx()
    secondary_canvas.plot(hours_interp, [x * 1000 / 3600 for x in wind_interp], linewidth=3.0, color='#4189e8')
    secondary_canvas.set_ylim(canvas.get_ylim()[0] * 1000 / 3600, canvas.get_ylim()[1] * 1000 / 3600)
    secondary_canvas.set_ylabel('Prędkość wiatru [m/s]')

    canvas.grid(True)


def generate_graphs_image():
    figure, axes = plt.subplots(3, 1, figsize=(10, 9))

    hours = ['10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21']

    graph_temperature(axes[0], hours)
    graph_rainfall(axes[1], hours)
    graph_wind(axes[2], hours)

    plt.tight_layout()
    plt.savefig('./assets/generated_images/graphs.png')


