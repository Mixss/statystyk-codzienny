import nextcord
from nextcord import slash_command, InteractionMessage
from nextcord.ext.commands import Cog, Bot

from ui import message_templates
from ui.utils import MessageEditHandler
from ui.views import StatsView


class CommandStats(Cog):

    def __init__(self, client: Bot):
        self.client = client

    @slash_command(name='stats', description='Wysyła ogólne informacje o dzisiejszym dniu')
    async def stats(self, interaction: nextcord.Interaction):
        forecast_image = nextcord.File('./assets/generated_images/image.png')
        message = await interaction.response.send_message(
            embed=message_templates.daily_stats_embed(forecast_image.filename), view=StatsView(self.client),
            files=[forecast_image])

        MessageEditHandler.last_message = await message.fetch()


def setup(bot):
    bot.add_cog(CommandStats(bot))
