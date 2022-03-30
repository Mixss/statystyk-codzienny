import csv
import math
import time
from datetime import date, datetime
import urllib.request, json

days_of_week = {
    0 : "poniedziałek",
    1 : "wtorek",
    2 : "środa",
    3 : "czwartek",
    4 : "piątek",
    5 : "sobota",
    6 : "niedziela"
}

true_forecast = True

def get_today():
    return date.today().strftime("%d.%m")

def get_imieniny_list():
    imieniny = {}
    with open("imieniny.csv") as file_imieniny:
        csv_reader = csv.reader(file_imieniny, delimiter=',')
        line_count = 0
        for row in csv_reader:
            imieniny[f"{row[0]}{row[1]}"] = row[2]
    return imieniny

def get_today_names():
    now = date.today().strftime("%d%m")
    names_string = get_imieniny_list()[now]
    names = names_string.split()
    result = ""
    for i in range(len(names)):
        result = result + names[i]
        if i < len(names) - 1:
            result = result + ", "

    return result

def get_day_of_the_year():
    return datetime.now().timetuple().tm_yday

def get_days_left_to_the_end_of_the_year():
    year = date.today().strftime("%y")
    days_in_year = 365
    if int(year) % 4 == 0:
        days_in_year = 366
    return days_in_year - get_day_of_the_year()

def get_week_of_the_year():
    return date.today().strftime("%V")

def get_day_of_week():
    day = datetime.today().weekday()
    return days_of_week[day]

def get_final_respond():
    sr, ss = get_sunset_sunrise()
    forecastText, minTemp, maxTemp, forecastInfo, raining, wind, air = get_forecast()
    rain_info = ""
    if raining:
        rain_info="\n*Możliwe opady atmosferyczne*"

    result = f"Statystyki na dzień **{get_today()}** ({get_day_of_week()}): \n" \
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

    return result

def get_sunset_sunrise():
    with urllib.request.urlopen("https://api.sunrise-sunset.org/json?lat=54.409724&lng=18.634314") as url:
        data = json.loads(url.read())
        sunrise = data["results"]["sunrise"]
        sunrise = sunrise[0:len(sunrise)-6]
        sunset = data["results"]["sunset"]
        sunset = sunset[0:len(sunset)-6]

        # add 12h and utc to sunset format
        if sunset[1] == ':':
            hour = int(sunset[0]) + 12 + get_utc_difference()
            sunset = sunset[1:4]
            sunset = f"{hour}{sunset}"

        # add utc to sunrise
        hour = int(sunrise[0]) + get_utc_difference()
        sunrise = sunrise[1:4]
        sunrise = f"{hour}{sunrise}"

    return sunrise, sunset

def get_utc_difference():
    return time.localtime().tm_hour - time.gmtime().tm_hour


def get_forecast():
    # https://worldweather.wmo.int/pl/json/25_pl.xml

    headline = "Chmury i słońce"
    minTemp = 4
    maxTemp = 11
    info = "Chmury i słońce"
    rain = False
    wind = 30
    air = "Dobre"


    if true_forecast:
        with urllib.request.urlopen("https://worldweather.wmo.int/pl/json/25_pl.xml") as url:
            data = json.loads(url.read())
            weather = data["city"]["forecast"]["forecastDay"][0]
            minTemp = weather["minTemp"]
            maxTemp = weather["maxTemp"]
            info = weather["weather"]


    return headline, minTemp, maxTemp, info, rain, wind, air




