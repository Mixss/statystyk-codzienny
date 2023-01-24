import csv
import json
import time
import urllib.request
from datetime import date, datetime, timedelta
import requests
from bs4 import BeautifulSoup


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

    return True, ''


def unset_default_channel(server_id):
    with open("data/config.json") as file:
        data = json.load(file)
    for el in data["BroadcastChannels"]:
        if el["ServerId"] == server_id:
            data["BroadcastChannels"].remove(el)
            with open("data/config.json", "w") as f:
                json.dump(data, f)
            return True, ''

    return False, 'Nie usunięto kanału domyślnego. Prawdopodobnie ten serwer nie posiada kanału domyślnego. Możesz go ' \
                  'ustawić za pomocą `/channel set`'


def get_default_channel(server_id) -> (bool, int, str):
    with open("data/config.json") as file:
        data = json.load(file)

    for el in data["BroadcastChannels"]:
        if el["ServerId"] == server_id:
            return True, el["ChannelId"], ''

    return False, -1, 'Ten serwer nie posiada kanału domyślnego. Możesz go ' \
                      'ustawić za pomocą `/channel set`'


def get_channels():
    with open("data/config.json") as file:
        data = json.load(file)

    return data["BroadcastChannels"]


days_of_week = {
    0: "poniedziałek",
    1: "wtorek",
    2: "środa",
    3: "czwartek",
    4: "piątek",
    5: "sobota",
    6: "niedziela"
}

moon_phases = {
    "New": ":new_moon:",
    "WaningCrescent": ":waning_crescent_moon:",
    "ThirdQuarter": ":last_quarter_moon:",
    "WaningGibbous": ":waning_gibbous_moon:",
    "Full": ":full_moon:",
    "WaxingGibbous": ":waxing_gibbous_moon:",
    "FirstQuarter": ":first_quarter_moon:",
    "WaxingCrescent": ":waxing_crescent_moon:"
}


def get_today():
    return date.today().strftime("%d.%m")


def get_imieniny_list():
    imieniny = {}
    with open("data/imieniny.csv", encoding="utf-8") as file_imieniny:
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


def get_sunset_sunrise():
    data = download_forecast(type="daily")
    sunrise = data["DailyForecasts"][0]["Sun"]["Rise"][11:16]
    sunset = data["DailyForecasts"][0]["Sun"]["Set"][11:16]

    return sunrise, sunset


def get_utc_difference():
    return time.localtime().tm_hour - time.gmtime().tm_hour


def download_forecast(type='daily'):
    if type == 'daily':
        with open("data/forecast_daily.json") as file:
            data = json.load(file)
        date_of_download = data["DailyForecasts"][0]["Date"][:10]
        todays_date = f"{datetime.today()}"[:10]

        if date_of_download != todays_date:
            # forecast data is outdated
            print("Downloading new file: forecast_daily.json")

            with urllib.request.urlopen(
                    "http://dataservice.accuweather.com/forecasts/v1/daily/1day/275174?apikey"
                    "=GZcekJNnnT8F1qo8VJteym6lRa54mH2b&language=pl-pl&details=true&metric=true") as url:
                data = json.loads(url.read())
                with open("data/forecast_daily.json", "w") as new_forecast:
                    json.dump(data, new_forecast)

        return data
    if type == 'hourly':
        with open("data/forecast_12_hours.json") as file:
            data = json.load(file)
        date_of_download = data[0]["DateTime"][:10]
        todays_date = f"{datetime.today()}"[:10]

        if date_of_download != todays_date:
            # forecast data is outdated
            print("Downloading new file: forecast_12_hours.json")

            with urllib.request.urlopen("http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/275174?apikey"
                                        "=GZcekJNnnT8F1qo8VJteym6lRa54mH2b&language=pl-pl&details=true&metric=true") \
                    as url:
                data = json.loads(url.read())
                with open("data/forecast_12_hours.json", "w") as new_forecast:
                    json.dump(data, new_forecast)

        return data

    return []


def get_daily_forecast():
    data = download_forecast(type='daily')

    headline = data["Headline"]["Text"]
    minTemp = round(data["DailyForecasts"][0]["Temperature"]["Minimum"]["Value"])
    maxTemp = round(data["DailyForecasts"][0]["Temperature"]["Maximum"]["Value"])
    info = data["DailyForecasts"][0]["Day"]["LongPhrase"]
    rain = data["DailyForecasts"][0]["Day"]["RainProbability"]
    air = data["DailyForecasts"][0]["AirAndPollen"][0]["Category"]
    uvindex = data["DailyForecasts"][0]["AirAndPollen"][5]["Value"]
    uvdanger = data["DailyForecasts"][0]["AirAndPollen"][5]["Category"]
    try:
        moon = moon_phases[data["DailyForecasts"][0]["Moon"]["Phase"]]
    except KeyError:
        moon = data["DailyForecasts"][0]["Moon"]["Phase"]

    return headline, minTemp, maxTemp, info, rain, air, uvindex, uvdanger, moon


def get_hourly_forecast():
    data = download_forecast(type='hourly')

    hours = []
    temperatures = []
    icons = []
    wind_speeds = []
    wind_directions = []

    for one_hour in data:
        hours.append(one_hour["DateTime"][11:13])
        temperatures.append(round(one_hour["Temperature"]["Value"]))
        icons.append(one_hour["WeatherIcon"])
        wind_speeds.append(one_hour["Wind"]["Speed"]["Value"])
        wind_directions.append(one_hour["Wind"]["Direction"]["Degrees"])

    return hours, temperatures, icons, wind_speeds, wind_directions


def get_advanced_hourly_forecast():
    data = download_forecast(type='hourly')

    result = {}

    for one_hour in data:
        pass


def get_current_weather():
    with urllib.request.urlopen("https://danepubliczne.imgw.pl/api/data/synop/station/gdansk") as url:
        data = json.loads(url.read())
    time_of_measurement = int(data["godzina_pomiaru"]) + get_utc_difference()
    temperature = round(float(data["temperatura"]))
    wind_speed = data["predkosc_wiatru"]
    fall = data["suma_opadu"]
    pressure = data["cisnienie"]

    return time_of_measurement, temperature, wind_speed, fall, pressure


def download_currencies(when='today'):
    to_list = []
    with urllib.request.urlopen(f"https://api.nbp.pl/api/exchangerates/rates/a/eur/{when}?format=json") as url:
        data_d = json.loads(url.read())
        to_list.append([data_d["code"], round(data_d["rates"][0]["mid"], 2)])
    with urllib.request.urlopen(f"https://api.nbp.pl/api/exchangerates/rates/a/usd/{when}?format=json") as url:
        data_d = json.loads(url.read())
        to_list.append([data_d["code"], round(data_d["rates"][0]["mid"], 2)])

    return to_list


def download_gas_prices():
    gas_prices = {}

    try:
        url = 'https://www.autocentrum.pl/paliwa/ceny-paliw/pomorskie/'

        response = requests.get(url)
    except:
        print('Gas prices response is not 200 OK, terminating function')
        return gas_prices

    soup = BeautifulSoup(response.text, 'html.parser')
    div = soup.find('div', {'class': 'fuels-wrapper'})

    contents = list(div.children)

    for fuel_type in contents:
        if not isinstance(fuel_type, type(contents[0])):
            fuel_type_text = fuel_type.text.splitlines()

            gas_prices[fuel_type_text[1]] = fuel_type_text[3].strip()

    gas_prices.pop('ON+')

    return gas_prices


def get_currencies():
    downloaded = False

    result = {
        "Values": [],
        "Messages": []
    }
    to_list = []
    try:
        to_list = download_currencies()

        downloaded = True
    except:
        yesterday = datetime.today() - timedelta(days=1)
        date_string = yesterday.strftime("%Y-%m-%d")

        try:
            to_list = download_currencies(f"{date_string}")

            downloaded = True
        except:
            # reading data from file
            with open("data/finances.json") as file:
                data = json.load(file)
            currencies = data["Currencies"]
            for currency in currencies:
                value = "{:.2f}".format(currency["Value"])
                to_list.append([currency["Code"], value])

    # saving data to a file
    with open("data/finances.json") as file:
        data = json.load(file)
    currencies = data["Currencies"]
    for currency in currencies:
        code = currency["Code"]
        for l in to_list:
            if l[0] == code:
                if downloaded:
                    currency["Value"] = l[1]
                result["Values"].append("{:.2f}".format(currency["Value"]))
                result["Messages"].append(currency["DiscordMessage"])

    return result


def get_deadlines():
    courses = []
    dates = []
    descriptions = []

    with open("./data/deadlines/exams.csv", encoding="utf-8") as file_exams_deadlines:
        csv_reader = csv.reader(file_exams_deadlines, delimiter=';')
        for row in csv_reader:
            courses.append(row[0])
            dates.append(row[1])
            descriptions.append(row[2])

    with open("./data/deadlines/projects.csv", encoding="utf-8") as file_projects_deadlines:
        csv_reader = csv.reader(file_projects_deadlines, delimiter=';')
        for row in csv_reader:
            courses.append(row[0])
            dates.append(row[1])
            descriptions.append(row[2])

    months = list(map(lambda x: x.split(' ')[2].split('.')[1], dates))
    days = list(map(lambda x: x.split(' ')[2].split('.')[0], dates))

    to_sort = list(zip(months, days, courses, dates, descriptions))
    to_sort.sort()
    months, days, courses, dates, descriptions = zip(*to_sort)

    return courses, dates, descriptions


def get_holiday():
    today = date.today()
    month = today.month
    day = today.day
    with urllib.request.urlopen(
            f"https://pniedzwiedzinski.github.io/kalendarz-swiat-nietypowych/{month}/{day}.json") as url:
        data = json.loads(url.read())

    holiday = data[0]['name']
    return holiday
