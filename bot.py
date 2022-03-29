import discord
from datetime import date, datetime
from discord.ext import commands, tasks

import stats
intents = discord.Intents().all()

client = commands.Bot(command_prefix='s!', intents=intents)

@client.event
async def on_ready():
    print("Bot started successfully")
    send_stats.start()


@client.command()
async def stat(ctx):
    await ctx.send(stats.get_final_respond())

@client.command()
async def chuj(ctx):
    await ctx.send("chuj")

async def send_message(message):
    channel = client.get_channel(958119472793780304) # kanał esovisco
    # channel = client.get_channel(828951713074380840) #kanał ewingi
    await channel.send(message)

@tasks.loop(minutes=30)
async def send_stats():
    now = datetime.now()
    hour = now.hour
    minute = now.minute
    if 6 <= hour < 7:
        if 15 <= minute < 45:
            print(f"{hour}:{minute} -> wysyłam poranne statystyki")
            await send_message(stats.get_final_respond())



