import nextcord
from nextcord.ext.commands import Bot
from nextcord.ui import View

from ui import message_templates
from ui.message_templates import deadlines_message_template, finances_message_template
from ui.utils import MessageEditHandler


class StatsView(View):

    def __init__(self, client: Bot):
        super().__init__()
        self.client = client

    last_view_state = 'main_page'

    @nextcord.ui.button(label='Strona główna', style=nextcord.ButtonStyle.danger)
    async def main_page(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if StatsView.last_view_state == 'main_page':
            return

        forecast_image = nextcord.File('./assets/generated_images/image.png')
        embed = await message_templates.daily_stats_embed(forecast_image.filename)
        await MessageEditHandler.last_message.edit(content='',
                                                   embed=embed,
                                                   view=StatsView(self.client), files=[forecast_image])

        MessageEditHandler.last_message = interaction.message

        StatsView.last_view_state = 'main_page'

    @nextcord.ui.button(label='Rozszerzona pogoda', style=nextcord.ButtonStyle.green)
    async def extended_forecast(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if StatsView.last_view_state == 'extended_forecast':
            return

        await MessageEditHandler.last_message.edit(content=':thermometer: **Rozszerzona prognoza pogody**', embed=None,
                                                   files=[nextcord.File('assets/generated_images/graphs.png')])
        MessageEditHandler.last_message = interaction.message

        StatsView.last_view_state = 'extended_forecast'

    @nextcord.ui.button(label='Finanse', style=nextcord.ButtonStyle.blurple)
    async def finances(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if StatsView.last_view_state == 'finances':
            return

        await MessageEditHandler.last_message.edit(content=finances_message_template(), embed=None, files=[])
        MessageEditHandler.last_message = interaction.message

        StatsView.last_view_state = 'finances'

    @nextcord.ui.button(label='Terminy', style=nextcord.ButtonStyle.blurple)
    async def deadlines(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if StatsView.last_view_state == 'deadlines':
            return
        await MessageEditHandler.last_message.edit(content=deadlines_message_template(), embed=None, files=[])
        MessageEditHandler.last_message = interaction.message

        StatsView.last_view_state = 'deadlines'
