import os
from dotenv import load_dotenv
import psycopg2
import psycopg2.extras

load_dotenv()
from get_bike_data import get_and_transform_bike_data
from get_weather_data import get_weather_data


def load_data():
    try:
        conn = psycopg2.connect(
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
            sslmode=os.getenv("DB_SSLMODE"),
        )
        cur = conn.cursor()

        insert_weather_data = """
        INSERT INTO weather_data (
            timestamp,
            temperature, relative_humidity, 
            apparent_temperature, is_day, 
            surface_pressure, pressure_msl, 
            precipitation, rain, snowfall, 
            wind_speed, showers, cloud_cover, 
            wind_direction
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """

        # insert_bike_stations_status = """
        # INSERT INTO bike_stations_status (
        #     station_id,
        #     timestamp,
        #     free_bikes,
        #     empty_slots
        # ) VALUES (%s, %s, %s, %s);
        # """

        insert_bike_stations_status = """
        INSERT INTO bike_stations_status (
            station_id,
            timestamp,
            free_bikes,
            empty_slots
        ) VALUES %s;
        """

        # insert_bike_stations = """
        # INSERT INTO bike_stations (
        #     id,
        #     name,
        #     lat,
        #     lon,
        #     slots
        # ) VALUES (%s, %s, %s, %s, %s)
        # ON CONFLICT (id) DO NOTHING;
        # """

        insert_bike_stations = """
        INSERT INTO bike_stations (
            id,
            name,
            lat,
            lon,
            slots
        ) VALUES %s
        ON CONFLICT (id) DO NOTHING;
        """

        weather_data = get_weather_data()
        weather_data_to_insert = (
            weather_data["time"],
            weather_data["temperature"],
            weather_data["humidity"],
            weather_data["apparent_temperature"],
            weather_data["is_day"],
            weather_data["surface_pressure"],
            weather_data["pressure_msl"],
            weather_data["precipitation"],
            weather_data["rain"],
            weather_data["snowfall"],
            weather_data["wind_speed"],
            weather_data["showers"],
            weather_data["cloud_cover"],
            weather_data["wind_direction"],
        )

        bike_data = get_and_transform_bike_data()
        # bike_stations_data_to_insert = (
        #     bike_data["id"],
        #     bike_data["name"],
        #     bike_data["lat"],
        #     bike_data["lon"],
        #     bike_data["slots"],
        # )
        bike_stations_data_to_insert = list(
            bike_data[["id", "name", "lat", "lon", "slots"]].itertuples(
                index=False, name=None
            )
        )

        # bike_stations_status_data_to_insert = (
        #     bike_data["timestamp"],
        #     bike_data["id"],
        #     bike_data["free_bikes"],
        #     bike_data["empty_slots"],
        # )
        bike_stations_status_data_to_insert = list(
            bike_data[["id", "timestamp", "free_bikes", "empty_slots"]].itertuples(
                index=False, name=None
            )
        )

        # 3. Execute and Commit
        cur.execute(insert_weather_data, weather_data_to_insert)
        psycopg2.extras.execute_values(
            cur, insert_bike_stations, bike_stations_data_to_insert
        )
        psycopg2.extras.execute_values(
            cur, insert_bike_stations_status, bike_stations_status_data_to_insert
        )
        # cur.execute(insert_bike_stations, bike_stations_data_to_insert)
        # cur.execute(insert_bike_stations_status, bike_stations_status_data_to_insert)
        conn.commit()
        print("Data inserted successfully")

    except Exception as e:
        print(f"Failed to insert record: {e}")
    finally:
        if conn:
            cur.close()
            conn.close()


if __name__ == "__main__":
    load_data()
