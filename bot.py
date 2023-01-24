from datetime import datetime
from logic.advanced_forecast import generate_graphs_image
from logic.forecast_image import generate_forecast_image


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


# sends stats to the channels defined i the file data/config.json
# to add a channel to the config run 'channel set' command on the channel
async def broadcast_stats():
    list = bc.get_channels()
    for el in list:
        channel_id = el["ChannelId"]
        channel = client.get_channel(channel_id)

        generate_forecast_image()
        await channel.send(bc.get_daily_stats_message())

        with open("assets/generated_images/image.png", 'rb') as f:
            picture = discord.File(f)
            await channel.send(file=picture)


# sends the same message to the channels defined i the file data/config.json
# to add a channel to the config run 'channel set' command on the channel
async def broadcast_message(message, image=None):
    list = bc.get_channels()
    for el in list:
        channel_id = el["ChannelId"]
        channel = client.get_channel(channel_id)
        await channel.send(message)
        if image is not None:
            await channel.send(file=image)


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

            generate_forecast_image()
            generate_graphs_image()

            await broadcast_stats()


@tasks.loop(hours=1)
async def generate_weather_image():
    generate_forecast_image()
    generate_graphs_image()

    print(f'Wygenerowano obraz - {datetime.now().hour}:{datetime.now().minute}')