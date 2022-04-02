import discord
from datetime import date, datetime

from discord.ext import commands, tasks
from discord.ui import Button, View
#
# from asyncio import TimeoutError

import stats
import bot_config as bc
from forecast_image import generate_forecast_image

intents = discord.Intents().all()

client = commands.Bot(command_prefix='s!', intents=intents)


@client.event
async def on_ready():
    await client.change_presence(
        activity=discord.Activity(type=discord.ActivityType.listening, name="Srogie Jaja Mikołaja"))
    print("Bot started successfully")
    send_stats.start()


@client.command()
async def button(ctx):
    button1 = Button(label="dupa", style=discord.ButtonStyle.green)
    button2 = Button(label="cipa", style=discord.ButtonStyle.grey)

    async def button_callback1(interaction):
        await interaction.response.send_message(f"{interaction.user.mention} chuj ci w dupe")

    async def button_callback2(interaction):
        await interaction.response.send_message(f"{interaction.user.mention} dobrze")

    button1.callback = button_callback1
    button2.callback = button_callback2

    view = View()
    view.add_item(button1)
    view.add_item(button2)
    await ctx.send("dupa", view=view)


@client.command(brief="- wysyła ogólne informacje o dzisiejszym dniu",
                description="Wysyła informacje na temat dzisiejszego dnia.\n"
                            "Informacje takie jak dzień w roku, imieniny, prognoza pogody i inne")
async def stats(ctx):
    generate_forecast_image()
    await ctx.send(bc.get_daily_stats_message())

    last_viewed_menu = 'main'  # other values: forecast, finances, deadlines

    button_main = Button(label='Strona główna', style=discord.ButtonStyle.red, custom_id='btnmain')
    button_forecast = Button(label='Rozszerzona pogoda', style=discord.ButtonStyle.green, custom_id='btnforecast')
    button_finances = Button(label='Finanse', style=discord.ButtonStyle.blurple, custom_id='btnfinances')
    button_deadlines = Button(label='Terminy', style=discord.ButtonStyle.blurple, custom_id='btndeadlines')

    async def button_main_callback(interaction):
        await clear_previous_message()
        nonlocal last_viewed_menu
        last_viewed_menu = 'main'
        await ctx.send(bc.get_daily_stats_message())
        with open("generated_images/image.png", 'rb') as file:
            pict = discord.File(file)
            await ctx.send(file=pict, view=view)
    button_main.callback = button_main_callback

    async def button_forecast_callback(interaction):
        await interaction.response.send_message(f"tu bedzie pogoda")
    button_forecast.callback = button_forecast_callback

    async def button_finances_callback(interaction):
        await interaction.response.send_message(f"tu beda finanse")
    button_finances.callback = button_finances_callback

    async def button_deadlines_callback(interaction):
        await clear_previous_message()
        nonlocal last_viewed_menu
        last_viewed_menu = 'deadlines'
        await ctx.send(bc.get_deadlines_message(), view=view)
    button_deadlines.callback = button_deadlines_callback

    async def clear_previous_message():
        if last_viewed_menu == 'main':
            to_delete = []
            counter = 0
            async for message in ctx.channel.history(limit=100):
                if message.author == client.user:
                    counter += 1
                to_delete.append(message)
                if counter == 2:
                    break

            for message in to_delete:
                await message.delete()
        else:
            last_message = await ctx.fetch_message(ctx.channel.last_message_id)
            await last_message.delete()

    view = View()
    view.add_item(button_main)
    view.add_item(button_forecast)
    view.add_item(button_finances)
    view.add_item(button_deadlines)

    with open("generated_images/image.png", 'rb') as f:
        picture = discord.File(f)
        await ctx.send(file=picture, view=view)


@client.command(brief="- says chuj")
async def chuj(ctx):
    await ctx.send("chuj")
    with open("generated_images/image.png", 'rb') as f:
        picture = discord.File(f)
        await ctx.send(file=picture)


@client.command(brief="- zarządzanie domyślnym kanałem",
                description="\nPozwala zarządzać domyślnym kanałem: \n"
                            "- channel set: ustawia wybrany kanał jako domyślny \n"
                            "- channel check: sprawdza, który kanał jest ustawiony jako domyślny\n"
                            "- channel unset: usuwa kanał domyślny\n")
async def channel(ctx, *args):
    if len(args) == 1:
        if args[0] == "check":
            await send_message(f"{ctx.message.author.mention} Ten kanał jest ustawiony jako domyślny.",
                               ctx.message.guild.id)
        elif args[0] == "set":
            await ctx.send("Ten kanał został ustawiony jako domyślny.")
            bc.set_default_channel(ctx.message.guild.id, ctx.message.channel.id)
        elif args[0] == "unset":
            if bc.unset_default_channel(ctx.message.guild.id):
                await ctx.send(
                    "Kanał nie jest już kanałem domyślnym. Jeżeli dalej chcesz otrzymywać codzienne statystyki "
                    "ustaw jeden z kanałów jako domyślny używając `s!channel set`")
            else:
                await ctx.send("Nie usunięto kanału domyślnego. Prawdopodobnie ten serwer nie posiada kanału "
                               "domyślnego. Możesz go ustawić za pomocą `s!channel set`")
        else:
            await ctx.send("Niepoprawny argument, użyj: `s!help channel`")
    else:
        await ctx.send("Niepoprawne użycie, użyj: `s!help channel`")


@client.command(brief="- pokazuje aktualną pogodę", description="Wyświetla aktualną pogodę w Gdańsku. \n Informacja "
                                                                "zawiera informacje o godzinie pomiaru, temperaturze,"
                                                                " prędkości wiatru, opadach i ciśnieniu.")
async def weather(ctx):
    await ctx.send(bc.get_current_weather_message())


@client.command(brief="- wyświetla najważniejsze terminy", description="Wyświetla terminy najbliższych kolokwiów, "
                                                                       "terminy oddania projektów")
async def terminy(ctx, *args):
    if len(args) >= 1:
        try:
            num_of_deadlines = int(args[0])

            if num_of_deadlines <= 0:
                await ctx.send("Niepoprawny argument, podaj liczbę większą od zera")
            else:
                await ctx.send(bc.get_deadlines_message(num_of_deadlines))
        except ValueError:
            await ctx.send("Niepoprawny argument, użyj: `s!help channel`")
    else:
        await ctx.send(bc.get_deadlines_message())



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
    if 4 <= hour < 5:
        if 15 <= minute < 45:
            print(f"{hour}:{minute} -> wysyłam pobrane statystyki")
            await broadcast_message(bc.get_daily_stats_message())
