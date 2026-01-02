from dotenv import load_dotenv
import openmeteo_requests
from datetime import datetime
import requests_cache
from retry_requests import retry

load_dotenv()


def get_weather_data():
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
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
        ],
        "timezone": "America/New_York",
        "forecast_days": 1,
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    # print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
    # print(f"Elevation: {response.Elevation()} m asl")
    # print(f"Timezone: {response.Timezone()}{response.TimezoneAbbreviation()}")
    # print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")

    # Process current data. The order of variables needs to be the same as requested.
    current = response.Current()
    data = {}
    data["timestamp"] = current.Time()
    data["time"] = datetime.fromtimestamp(data["timestamp"]).strftime(
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
    return data
