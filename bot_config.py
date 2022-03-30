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
    forecastText, minTemp, maxTemp, forecastInfo, raining, wind, air = get_daily_forecast()

    message = f"Statystyki na dzień **{get_today()}** ({get_day_of_week()}): \n" \
              f" \n" \
              f":date: Jest to **{get_day_of_the_year()}** dzień w roku i **{get_week_of_the_year()}** tydzień roku, " \
              f"pozostało **{get_days_left_to_the_end_of_the_year()}** dni do końca roku, \n" \
              f" \n" \
              f"Wschód słońca:  :sunrise:  **{sr}**\n" \
              f"Zachód słońca:  :city_sunset:   **{ss}**\n" \
              f" \n" \
              f"Imieniny: :couple: *{get_today_names()}* \n" \
              f" \n" \
              f" :white_sun_cloud: **Prognoza pogody**\n" \
              f" :thermometer: Temperatura:\n" \
              f" > :snowflake: min: **{minTemp} °C**\n" \
              f" > :fire: max: **{maxTemp} °C**\n" \
              f" \n:white_sun_small_cloud: Spodziewana pogoda: \n" \
              f"*{forecastInfo}*" \
              f" \n" \
              f""

    return message


def get_current_weather_message():
    tom, temp, wind_s, fall, press = get_current_weather()

    message = f"**Aktualna pogoda** (pomiar *{tom}:00*):\n\n" \
              f":thermometer: Temperatura **{temp} °C**\n" \
              f":dash: Prędkość wiatru: **{wind_s}** km/h \n" \
              f":cloud_rain: Opady: **{fall}** mm/h \n" \
              f":clock: Ciśnienie: **{press}** hPa"

    return message
