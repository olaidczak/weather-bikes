import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

def get_data2():
    connection = psycopg2.connect(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        sslmode=os.getenv("DB_SSLMODE"),
    )

    cur = connection.cursor()
    cur.execute("SELECT * FROM weather_data;")

    rows = cur.fetchall()
    colnames = [desc[0] for desc in cur.description]

    df = pd.DataFrame(rows, columns=colnames)

    cur.close()
    connection.close()
    return df


if __name__ == "__main__":
    df = get_data2()
    weather_hm = df.copy()
    weather_hm["date"] = weather_hm["timestamp"].dt.date
    weather_hm["hour"] = weather_hm["timestamp"].dt.hour
    weather_hm.groupby(["date", "hour"]).size().describe()
    print(weather_hm["temperature"])
