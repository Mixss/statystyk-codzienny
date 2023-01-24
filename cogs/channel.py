import nextcord
from nextcord import slash_command, SlashOption
from nextcord.ext.commands import Cog, Bot

from logic.logic import set_default_channel, unset_default_channel
from ui.message_templates import current_weather_message_template


class CommandChannel(Cog):

    def __init__(self, client: Bot):
        self.client = client

    @slash_command(name='channel', description='Umożliwia zarządzanie domyślnym kanałem')
    async def channel(self, interaction: nextcord.Interaction, mode = SlashOption(
        name='mode', choices={'set': 'set', 'unset': 'unset', 'check': 'check'})):

        if mode == 'set':
            status, error_message = set_default_channel(interaction.guild_id, interaction.channel_id)
            if not status:
                await interaction.response.send_message(error_message)
                return

            await interaction.response.send_message('Ten kanał został ustawiony jako domyślny.')

        elif mode == 'unset':
            status, error_message = unset_default_channel(interaction.guild_id)
            if not status:
                await interaction.response.send_message(error_message)
                return

            await interaction.response.send_mesage('Kanał nie jest już kanałem domyślnym. Jeżeli dalej chcesz '
                                                   'otrzymywać codzienne statystyki ustaw jeden z kanałów jako '
                                                   'domyślny używając `/channel set')

        elif mode == 'check':
            status, error_message = unset_default_channel(interaction.guild_id)
            if not status:
                await interaction.response.send_message(error_message)
                return

            await interaction.response.send_message(f'{interaction.message.author.mention} Ten kanał jest ustawiony '
                                                    f'jako domyślny.')






def setup(bot):
    bot.add_cog(CommandChannel(bot))
