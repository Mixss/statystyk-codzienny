import nextcord
from nextcord import slash_command
from nextcord.ext.commands import Cog, Bot

from ui.message_templates import current_weather_message_template


class CommandWeather(Cog):

    def __init__(self, client: Bot):
        self.client = client

    @slash_command(name='weather', description='Wyświetla aktualną pogodę w Gdańsku')
    async def weather(self, interaction: nextcord.Interaction):
        await interaction.response.send_message(embed=current_weather_message_template())


def setup(bot):
    bot.add_cog(CommandWeather(bot))
