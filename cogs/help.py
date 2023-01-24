import nextcord
from nextcord import slash_command, SlashOption
from nextcord.ext.commands import Cog, Bot

from logic.logic import set_default_channel, unset_default_channel, get_default_channel
from ui.message_templates import help_message_embed


class CommandHelp(Cog):

    def __init__(self, client: Bot):
        self.client = client

    @slash_command(name='help', description='Wyświetla dostępne komendy')
    async def help(self, interaction: nextcord.Interaction):
        await interaction.response.send_message(embed=help_message_embed())


def setup(bot):
    bot.add_cog(CommandHelp(bot))
