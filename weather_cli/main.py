import json
import os
import time

import requests
import typer
from dotenv import load_dotenv
from yaspin import yaspin

app = typer.Typer()
load_dotenv()


def load_translation():
    lang = os.getenv("TOOL_LANGUAGE", "en")
    try:
        with open(f"locales/{lang}.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Translation file for '{lang}' not found. Falling back to English.")
        with open("locales/en.json", "r", encoding="utf-8") as file:
            return json.load(file)


translations = load_translation()

api_key = os.getenv("API_KEY")
lang = os.getenv("TOOL_LANGUAGE", "en")
temp_unit_pref = os.getenv("TEMPERATURE_UNIT", "celsius")


@app.command()
def weather(city: str):
    spinner = yaspin()
    spinner.start()
    time.sleep(1)
    spinner.stop()

    res = requests.get(
        f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&lang={lang}"
    )
    data = res.json()

    # Determine temperature values based on unit preference
    if temp_unit_pref == "fahrenheit":
        temp = data["current"]["temp_f"]
        feels_like = data["current"]["feelslike_f"]
        temp_unit = "F"
    else:
        temp = data["current"]["temp_c"]
        feels_like = data["current"]["feelslike_c"]
        temp_unit = "C"

    weather_data = {
        "name": data["location"]["name"],
        "region": data["location"]["region"],
        "country": data["location"]["country"],
        "lat": data["location"]["lat"],
        "lon": data["location"]["lon"],
        "localtime": data["location"]["localtime"],
        "temp": temp,
        "feels_like": feels_like,
        "temp_unit": temp_unit,
        "condition": data["current"]["condition"]["text"],
        "humidity": data["current"]["humidity"],
        "pressure": data["current"]["pressure_mb"],
        "wind_speed": data["current"]["wind_kph"],
        "wind_dir": data["current"]["wind_dir"],
        "precipitation": data["current"]["precip_mm"],
        "uv_index": data["current"]["uv"],
    }

    print("\n")
    print(translations["weather-info"]["location"].format(**weather_data))
    print(translations["weather-info"]["localtime"].format(**weather_data))
    print(translations["weather-info"]["temperature"].format(**weather_data))
    print(translations["weather-info"]["condition"].format(**weather_data))
    print(translations["weather-info"]["humidity"].format(**weather_data))
    print(translations["weather-info"]["pressure"].format(**weather_data))
    print(translations["weather-info"]["wind"].format(**weather_data))
    print(translations["weather-info"]["precipitation"].format(**weather_data))
    print(translations["weather-info"]["uv"].format(**weather_data))
    print("\n")


if __name__ == "__main__":
    app()
