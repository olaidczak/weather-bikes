import requests
import pandas as pd
from datetime import datetime


def get_bike_data():
    url = "https://api.citybik.es/v2/networks/citi-bike-nyc"

    response = requests.get(url)
    bike_data = None
    if response.status_code == 200:
        bike_data = response.json()
    return bike_data


def filter_bike_data(data: dict):
    network = data.get("network", {})
    stations = network.get("stations", [])
    filtered = []
    for s in stations:
        filtered.append(
            {
                "id": s.get("id"),
                "timestamp": s.get("timestamp"),
                "name": s.get("name"),
                "lat": s.get("latitude"),
                "lon": s.get("longitude"),
                "free_bikes": s.get("free_bikes"),
                "empty_slots": s.get("empty_slots"),
                "slots": (s.get("extra") or {}).get("slots"),
            }
        )

    return filtered


def transform_to_df(data: list):
    df = pd.json_normalize(data)
    df["timestamp"] = pd.to_datetime(
        df["timestamp"], format="%Y-%m-%dT%H:%M:%S.%f%zZ", utc=True
    )
    return df


def get_and_transform_bike_data():
    raw_data = get_bike_data()
    filtered_data = filter_bike_data(raw_data)
    df = transform_to_df(filtered_data)
    return df
