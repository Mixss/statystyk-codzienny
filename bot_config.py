import json
from stats import *


def set_default_channel(server_id, channel_id):
    with open("data/config.json") as file:
        data = json.load(file)
    # check if config contains this server
    contains = False
    for el in data["BroadcastChannels"]:
        if el["ServerId"] == server_id:
            el["ChannelId"] = channel_id
            contains = True
            break
    if not contains:
        data["BroadcastChannels"].append({
            "ServerId": server_id,
            "ChannelId": channel_id
        })
    with open("data/config.json", "w") as f:
        json.dump(data, f)


def unset_default_channel(server_id):
    with open("data/config.json") as file:
        data = json.load(file)
    for el in data["BroadcastChannels"]:
        if el["ServerId"] == server_id:
            data["BroadcastChannels"].remove(el)
            with open("data/config.json", "w") as f:
                json.dump(data, f)
            return True
    return False


def get_channels():
    with open("data/config.json") as file:
        data = json.load(file)

    return data["BroadcastChannels"]


def get_daily_stats_message():
    sr, ss = get_sunset_sunrise()
    forecastText, minTemp, maxTemp, forecastInfo, raining, air, uvidex, uvdanger, moon_phase = get_daily_forecast()
    euro, usd = get_currencies()

    message = f"Statystyki na dzień **{get_today()}** ({get_day_of_week()}): \n" \
              f" \n" \
              f":date: Jest to **{get_day_of_the_year()}** dzień w roku i **{get_week_of_the_year()}** tydzień roku, " \
              f"pozostało **{get_days_left_to_the_end_of_the_year()}** dni do końca roku, \n" \
              f" \n" \
              f"Wschód słońca:  :sunrise:  **{sr}**\n" \
              f"Zachód słońca:  :city_sunset:   **{ss}**\n" \
              f" \n" \
              f"Faza księżyca:   {moon_phase}\n" \
              f" \n" \
              f"Imieniny: :couple: *{get_today_names()}* \n" \
              f" \n" \
              f":mask: Jakość powietrza: *{air}* \n" \
              f":sunglasses: Index UV: **{uvidex}** ({uvdanger}) \n " \
              f" \n" \
              f" :white_sun_cloud: **Prognoza pogody**\n" \
              f""

    # f":moneybag: Finanse: \n" \
    # f":euro: 1 EUR = **{euro}** PLN\n" \
    # f":dollar: 1 USD = **{usd}** PLN\n" \

    # f" :white_sun_cloud: **Prognoza pogody**\n" \
    # f" :thermometer: Temperatura:\n" \
    # f" > :snowflake: min: **{minTemp} °C**\n" \
    # f" > :fire: max: **{maxTemp} °C**\n" \
    # f" \n:white_sun_small_cloud: Spodziewana pogoda: \n" \
    # f"*{forecastInfo}* \n" \
    # f"*Prawdopodobieństwo deszczu:*  **{raining}%** \n\n" \

    return message


def get_current_weather_message():
    tom, temp, wind_s, fall, press = get_current_weather()

    message = f"**Aktualna pogoda** (pomiar *{tom}:00*):\n\n" \
              f":thermometer: Temperatura **{temp} °C**\n" \
              f":dash: Prędkość wiatru: **{wind_s}** km/h \n" \
              f":cloud_rain: Opady: **{fall}** mm/h \n" \
              f":clock: Ciśnienie: **{press}** hPa"

    return message


def get_deadlines_message(number_of_deadlines=5):
    courses, dates, descriptions = get_deadlines()

    text = ""
    if number_of_deadlines == 1:
        text = "najbliższy ważny termin"
    elif number_of_deadlines == 3 or number_of_deadlines == 4:
        text = "najbliższe ważne terminy"
    else:
        text = "najbliższych ważnych terminów"

    message = f':flushed: **{number_of_deadlines} {text}**\n\n'

    for course, date, desc in zip(courses[:number_of_deadlines], dates[:number_of_deadlines],
                                  descriptions[:number_of_deadlines]):
        message += f'**{course}**  -  {date}\n'
        message += f'*`{desc}`*\n\n'

    return message


def get_finances_message():
    currencies = get_currencies()

    message = f":moneybag: Finanse: \n\n"
    for i in range(len(currencies)):
        m = currencies['Messages'][i]
        for j in range(len(m)-1):
            if m[j] == ';' and m[j+1] == ';':
                end = m[(j+2):]
                begin = m[:(j)]
                # m = f"{currencies['Messages'][i]} = {currencies['Values'][i]} PLN\n"
                m = begin + str(currencies['Values'][i]) + end + "\n"
                break
        message = message + m
    return message


