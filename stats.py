import csv
import math
from datetime import date, datetime
import urllib.request, json

UTC_DIFFERENCE = 2

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
             f"{rain_info}\n" \
             f" \n" \
             f":dash: Jakość powietrza: *{air}*\n" \
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
            hour = int(sunset[0]) + 12 + UTC_DIFFERENCE
            sunset = sunset[1:4]
            sunset = f"{hour}{sunset}"

        # add utc to sunrise
        hour = int(sunrise[0]) + UTC_DIFFERENCE
        sunrise = sunrise[1:4]
        sunrise = f"{hour}{sunrise}"

    return sunrise, sunset

def get_forecast():
    if true_forecast:
        with urllib.request.urlopen("http://dataservice.accuweather.com/forecasts/v1/daily/1day/275174?apikey"
                                    "=GZcekJNnnT8F1qo8VJteym6lRa54mH2b&language=pl-pl&details=true&metric=true") as url:
            data = json.loads(url.read())
            headline = data["Headline"]["Text"]
            minTemp = math.floor(data["DailyForecasts"][0]["Temperature"]["Minimum"]["Value"])
            maxTemp = math.floor(data["DailyForecasts"][0]["Temperature"]["Maximum"]["Value"])
            info = data["DailyForecasts"][0]["Day"]["LongPhrase"]
            rain = data["DailyForecasts"][0]["Day"]["HasPrecipitation"]
            wind = data["DailyForecasts"][0]["Day"]["Wind"]["Speed"]["Value"]
            air = data["DailyForecasts"][0]["AirAndPollen"][0]["Category"]
            print(air)
    else:
        headline= "Chmury i słońce"
        minTemp = 4
        maxTemp = 11
        info = "Chmury i słońce"
        rain = False
        wind = 30
        air = "Dobre"

    return headline, minTemp, maxTemp, info, rain, wind, air




