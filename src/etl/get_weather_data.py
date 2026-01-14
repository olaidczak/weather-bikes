from dotenv import load_dotenv
import openmeteo_requests
import requests_cache
from retry_requests import retry
from datetime import datetime, timezone


def get_weather_data():
    cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 40.7143,
        "longitude": -74.006,
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "is_day",
            "surface_pressure",
            "pressure_msl",
            "precipitation",
            "rain",
            "snowfall",
            "wind_speed_10m",
            "showers",
            "cloud_cover",
            "wind_direction_10m",
            "weather_code",
        ],
        "timezone": "America/New_York",
        "forecast_days": 1,
    }
    responses = openmeteo.weather_api(url, params=params)

    response = responses[0]
    current = response.Current()
    data = {}
    data["timestamp"] = current.Time()
    data["time"] = datetime.fromtimestamp(data["timestamp"], tz=timezone.utc).strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    data["temperature"] = current.Variables(0).Value()
    data["humidity"] = current.Variables(1).Value()
    data["apparent_temperature"] = current.Variables(2).Value()
    data["is_day"] = bool(current.Variables(3).Value())
    data["surface_pressure"] = current.Variables(4).Value()
    data["pressure_msl"] = current.Variables(5).Value()
    data["precipitation"] = current.Variables(6).Value()
    data["rain"] = current.Variables(7).Value()
    data["snowfall"] = current.Variables(8).Value()
    data["wind_speed"] = current.Variables(9).Value()
    data["showers"] = current.Variables(10).Value()
    data["cloud_cover"] = current.Variables(11).Value()
    data["wind_direction"] = current.Variables(12).Value()
    data["weather_code"] = current.Variables(13).Value()

    return data
