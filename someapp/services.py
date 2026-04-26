import json
from urllib.parse import urlencode
from urllib.request import urlopen
from urllib.error import URLError, HTTPError


GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

WEATHER_CODES = {
    0: "Clear sky",
    1: "Mostly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Heavy Drizzle",
    61: "Light rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Light snowfall",
    73: "Moderate snowfall",
    75: "Heavy snowfall",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Heavy rain showers",
    95: "Thunderstorm",
}


class WeatherServiceError(Exception):
    pass


def fetch_json(base_url, params):
    url = f"{base_url}?{urlencode(params)}"
    try:
        with urlopen(url, timeout=10) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError:
        raise WeatherServiceError("Błąd odpowiedzi z API pogodowego.")
    except URLError:
        raise WeatherServiceError("Nie udało się połączyć z API pogodowym.")


def get_current_weather(city):
    geo_data = fetch_json(
        GEOCODING_URL,
        {
            "name": city,
            "count": 1,
            "language": "pl",
            "format": "json",
        },
    )

    results = geo_data.get("results")
    if not results:
        raise WeatherServiceError("Nie znaleziono takiego miasta.")

    place = results[0]

    latitude = place["latitude"]
    longitude = place["longitude"]

    weather_data = fetch_json(
        FORECAST_URL,
        {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m",
            "timezone": "auto",
        },
    )

    current = weather_data.get("current", {})
    units = weather_data.get("current_units", {})
    weather_code = current.get("weather_code")

    return {
        "city": place.get("name"),
        "country": place.get("country"),
        "latitude": latitude,
        "longitude": longitude,
        "temperature": current.get("temperature_2m"),
        "temperature_unit": units.get("temperature_2m", "°C"),
        "apparent_temperature": current.get("apparent_temperature"),
        "humidity": current.get("relative_humidity_2m"),
        "humidity_unit": units.get("relative_humidity_2m", "%"),
        "wind_speed": current.get("wind_speed_10m"),
        "wind_speed_unit": units.get("wind_speed_10m", "km/h"),
        "weather_code": weather_code,
        "weather_description": WEATHER_CODES.get(weather_code, "Brak opisu"),
        "time": current.get("time"),
    }
