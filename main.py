import nextcord
from nextcord.ext import commands
from nextcord import Intents

from utils import utils
from utils.utils import generate_images, send_stats, BotObjectHolder

activity = nextcord.Activity(name='/help', type=nextcord.ActivityType.listening)
client = commands.Bot(command_prefix='s!', intents=Intents().all(), activity=activity)


@client.event
async def on_ready():
    print('\nClient started successfully')
    send_stats.start()


def bot_run():
    """starts basic bot configuration like loading commands and establishing bot connection"""

    token = utils.get_client_token()
    if token is None:
        raise KeyError(f'Failed to get configuration key. Env variable \'CLIENT_TOKEN\' not found')

    print('client: loading extensions:')
    utils.load_extensions(client)

    generate_images()

    BotObjectHolder.set_bot(client)

    client.run(token)


bot_run()
