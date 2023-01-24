from datetime import datetime, timedelta

import nextcord

from logic.logic import get_sunset_sunrise, get_currencies, get_holiday, get_daily_forecast, get_today, get_day_of_week, \
    get_day_of_the_year, get_days_left_to_the_end_of_the_year, get_week_of_the_year, get_today_names, get_deadlines, \
    download_gas_prices, get_current_weather


def daily_stats_embed(image_path):
    _, _, _, _, _, air_quality, uvidex, _, moon_phase = get_daily_forecast()

    embed = nextcord.Embed(title=f'Statystyki na dzień **{get_today()}** ({get_day_of_week()}):',
                           description=f'📅 Jest to **{get_day_of_the_year()}** dzień w roku i'
                                       f' **{get_week_of_the_year()}** tydzień roku, '
                                       f'pozostało **{get_days_left_to_the_end_of_the_year()}** dni do końca roku\n‎')

    embed.add_field(name='🥂 Dzisiejsze święto', value=get_holiday() + '\n‎', inline=False)

    embed.add_field(name='🌅 Wschód słońca', value=get_sunset_sunrise()[0] + '\n‎', inline=True)
    embed.add_field(name='🌇 Zachód słońca', value=get_sunset_sunrise()[1] + '\n‎', inline=True)

    embed.add_field(name='👫 Imieniny', value=get_today_names() + '\n‎', inline=True)
    embed.add_field(name='Faza księżyca', value=moon_phase + '\n‎', inline=True)

    embed.add_field(name='😷 Jakość powietrza', value=air_quality + '\n‎', inline=True)
    embed.add_field(name='😎 Index UV', value=str(uvidex) + '\n‎', inline=True)

    embed.add_field(name='⛅ Prognoza pogody', value=' ', inline=False)

    embed.set_image('attachment://' + image_path)

    return embed


def deadlines_message_template(number_of_deadlines=5):
    courses, dates, descriptions = get_deadlines()

    if len(courses) < number_of_deadlines:
        number_of_deadlines = len(courses)

    text = ""
    if number_of_deadlines == 1:
        text = "Najbliższy ważny termin"
        message = f':flushed: **{text}**\n\n'
    elif number_of_deadlines == 2 or number_of_deadlines == 3 or number_of_deadlines == 4:
        text = "najbliższe ważne terminy"
        message = f':flushed: **{number_of_deadlines} {text}**\n\n'
    else:
        text = "najbliższych ważnych terminów"
        message = f':flushed: **{number_of_deadlines} {text}**\n\n'

    for course, date, desc in zip(courses[:number_of_deadlines], dates[:number_of_deadlines],
                                  descriptions[:number_of_deadlines]):
        message += f'**{course}**  -  {date}\n'
        message += f'*`{desc}`*\n\n'

    return message


def finances_message_template():
    class Gasprices:
        gas_prices = download_gas_prices()
        last_gas_prices_download = datetime.now()

    currencies = get_currencies()

    if datetime.now() - Gasprices.last_gas_prices_download > timedelta(days=1):
        print('downloading gas prices')
        Gasprices.gas_prices = download_gas_prices()

    message = f":moneybag: Finanse: \n\n"
    for i in range(len(currencies)):
        m = currencies['Messages'][i]
        for j in range(len(m) - 1):
            if m[j] == ';' and m[j + 1] == ';':
                end = m[(j + 2):]
                begin = m[:(j)]
                m = begin + str(currencies['Values'][i]) + end + "\n"
                break
        message = message + m

    message += '\n\n:fuelpump: Ceny paliw (średnia cen na pomorzu):\n\n'

    for fuel_type in Gasprices.gas_prices.items():
        message += f'{fuel_type[0]}: **{fuel_type[1]}** PLN\n'

    return message


def current_weather_message_template():
    tom, temp, wind_s, fall, press = get_current_weather()

    message = f"**Aktualna pogoda** (pomiar *{tom}:00*):\n\n" \
              f":thermometer: Temperatura **{temp} °C**\n" \
              f":dash: Prędkość wiatru: **{wind_s}** km/h \n" \
              f":cloud_rain: Opady: **{fall}** mm/h \n" \
              f":clock: Ciśnienie: **{press}** hPa"

    embed = nextcord.Embed(title=f'Aktualna pogoda (pomiar {tom}:00)')

    embed.add_field(name=f'🌡️ Temperatura: **{temp} °C**', value=' ', inline=False)
    embed.add_field(name=f'💨 Prędkość wiatru: **{wind_s}** km/h', value=' ', inline=False)
    embed.add_field(name=f'🌧️ Opady: **{fall}** mm/h', value=' ', inline=False)
    embed.add_field(name=f'🕰 Ciśnienie: **{press}** hPa', value=' ', inline=False)

    return embed
