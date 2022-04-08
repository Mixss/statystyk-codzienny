import matplotlib as mp
import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import make_interp_spline, BSpline

INTERPOLATION_COEFFICIENT = 20


def interpolate_line(x, y, k_coeff):
    x_arr = np.array(x).astype(float)
    y_arr = np.array(y).astype(float)

    new_x = np.linspace(x_arr.min(), x_arr.max(), INTERPOLATION_COEFFICIENT * x_arr.size)

    spline = make_interp_spline(x_arr, y_arr, k=k_coeff)
    y_smooth = spline(new_x)

    return new_x, y_smooth


def graph_temperature(canvas):
    temperatures = [-4.5, -2., 0., 5., 2., 1., -0.3, 1.7, 1.9, 6.9, 7.8, 3.0]
    temperatures_felt = [-5.3, -3.2, -1.0, 2.0, 1.0, -0.8, 1.3, -1.5, 0.1, 4.2, 5.0, 3.8]

    hours = ['10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21']

    _, temperatures_interp = interpolate_line(hours, temperatures, 3)
    hours_extended, temperatures_felt_interp = interpolate_line(hours, temperatures_felt, 3)

    canvas.plot(hours_extended, temperatures_interp, label="Temperatura rzeczywista")
    canvas.plot(hours_extended, temperatures_felt_interp, label="Temperatura odczuwalna")
    canvas.legend(fontsize=12)

    canvas.grid(True)

    return canvas


def generate_graphs_image():
    figure, axes = plt.subplots(2, 1, figsize=(8, 10))

    axes[0] = graph_temperature(axes[0])

    plt.savefig('./assets/generated_images/graphs.png')

