import matplotlib as mp
from matplotlib import pyplot as plt


def graph_temperature(canvas):
    temperatures = [-4.5, -2., 0., 5., 2., 1., -0.3, 1.7, 1.9, 6.9, 7.8, 3.0]

    hours = ['10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21']

    canvas.plot(hours, temperatures)
    canvas.grid = True

    return canvas


def generate_graphs_image():
    figure, axes = plt.subplots(2, 1, figsize=(10, 6))

    axes[0] = graph_temperature(axes[0])

    plt.savefig('./generated_images/graphs.png')


generate_graphs_image()