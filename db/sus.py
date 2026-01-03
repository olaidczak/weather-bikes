import openmeteo_requests
import requests_cache
from retry_requests import retry
from datetime import datetime, timezone
import csv
import os

CSV_FILE = "weather_data.csv"

def append_to_csv(data: dict):
    file_exists = os.path.isfile(CSV_FILE)

    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data.keys())

        # Write header only once
        if not file_exists:
            writer.writeheader()

        writer.writerow(data)

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
            # "relative_humidity_2m",
            # "apparent_temperature",
            # "is_day",
            # "surface_pressure",
            # "pressure_msl",
            # "precipitation",
            # "rain",
            # "snowfall",
            # "wind_speed_10m",
            # "showers",
            # "cloud_cover",
            # "wind_direction_10m",
            # "weather_code",
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
    data["time_fetched_poland"] = data["time_fetched_poland"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data["temperature"] = current.Variables(0).Value()

    return data

if __name__ == "__main__":
    data = get_weather_data()
    append_to_csv(data)
    # print(data["timestamp"], data["time"])