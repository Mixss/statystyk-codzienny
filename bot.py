import discord
from datetime import date, datetime
from discord.ext import commands, tasks

import stats
import bot_config as bc
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
        await send_message(f"{ctx.message.author.mention} Ten kanał jest ustawiony jako domyślny.", ctx.message.guild.id)
    elif arg1 == "set":
        await ctx.send("Ten kanał został ustawiony jako domyślny.")
        bc.set_default_channel(ctx.message.guild.id, ctx.message.channel.id)
    else:
        await ctx.send("Nie poprawna komenda, użyj: s!help channel")

# sends the same message to the channels defined i the file data/config.json
# to add a channel to the config run 'channel set' command on the channel
async def broadcast_message(message):
    list = bc.get_channels()
    for el in list:
        channel_id = el["ChannelId"]
        channel = client.get_channel(channel_id)
        await channel.send(message)

# sends message to a 'default' channel defined in config.json
async def send_message(message, server_id):
    list = bc.get_channels()
    for el in list:
        if el["ServerId"] == server_id:
            channel = client.get_channel(el["ChannelId"])
            await channel.send(message)
            break

@tasks.loop(minutes=30)
async def send_stats():
    now = datetime.now()
    hour = now.hour
    minute = now.minute
    if 6 - stats.get_utc_difference() <= hour < 7 - stats.get_utc_difference():
        if 15 <= minute < 45:
            print(f"{hour}:{minute} -> wysyłam poranne statystyki")
            await broadcast_message(stats.get_final_respond())






