import discord
from datetime import date, datetime
from discord.ext import commands, tasks

import stats
import bot_config
intents = discord.Intents().all()

client = commands.Bot(command_prefix='s!', intents=intents)

@client.event
async def on_ready():
    print("Bot started successfully")
    send_stats.start()


@client.command(brief="- ends general information about this day")
async def stat(ctx):
    await ctx.send(stats.get_final_respond())

@client.command(brief="- says chuj")
async def chuj(ctx):
    await ctx.send("chuj")

@client.command()
async def channel(ctx, arg1):

    if arg1 == "test":
        await send_message(f"Statystyk jest ustawiony na ten kanał")
    elif arg1 == "set":
        await ctx.send("Ten kanał został ustawiony jako domyślny.")
        bot_config.set_default_channel(ctx.message.guild.id, ctx.message.channel.id)
    else:
        await ctx.send("Nie poprawna komenda, użyj: s!help channel")

async def send_message(message):
    channel = client.get_channel(958119472793780304) # kanał esovisco
    # channel = client.get_channel(828951713074380840) #kanał ewingi
    await channel.send(message)

@tasks.loop(minutes=30)
async def send_stats():
    now = datetime.now()
    hour = now.hour
    minute = now.minute
    if 6 - stats.get_utc_difference() <= hour < 7 - stats.get_utc_difference():
        if 15 <= minute < 45:
            print(f"{hour}:{minute} -> wysyłam poranne statystyki")
            await send_message(stats.get_final_respond())



