import os

from advanced_forecast import generate_graphs_image
from forecast_image import generate_forecast_image


def get_client_token():
    return os.getenv('CLIENT_TOKEN')


def load_extensions(client):
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and filename != '__init__.py':
            client.load_extension(f'cogs.{filename[:-3]}')
            print(f'    {filename[:-3]}')


def generate_images():
    generate_forecast_image()
    generate_graphs_image()
