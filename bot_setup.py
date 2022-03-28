import hikari
import lightbulb

import stats

bot = lightbulb.BotApp(token='OTU3OTYxMDg5NzIxNzI0OTY4.YkGYyQ.AxfC0a-LxMGBexV5bIyaah8sFiQ')

@bot.listen(hikari.StartedEvent)
async def on_start(event):
    pass

@bot.command
@lightbulb.command("stat", "Wyświetla informacje o dzisiejszym dniu")
@lightbulb.implements(lightbulb.SlashCommand)
async def stat(ctx):
    await ctx.respond(stats.get_final_respond())


