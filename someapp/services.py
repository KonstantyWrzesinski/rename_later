import json
from urllib.parse import urlencode
from urllib.request import urlopen
from urllib.error import URLError, HTTPError


GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

WEATHER_CODES = {
    0: "Bezchmurnie",
    1: "Przeważnie bezchmurnie",
    2: "Częściowe zachmurzenie",
    3: "Pochmurno",
    45: "Mgła",
    48: "Mgła osadzająca szadź",
    51: "Lekka mżawka",
    53: "Umiarkowana mżawka",
    55: "Silna mżawka",
    61: "Słaby deszcz",
    63: "Umiarkowany deszcz",
    65: "Silny deszcz",
    71: "Słabe opady śniegu",
    73: "Umiarkowane opady śniegu",
    75: "Silne opady śniegu",
    80: "Przelotne słabe opady",
    81: "Przelotne umiarkowane opady",
    82: "Przelotne silne opady",
    95: "Burza",
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