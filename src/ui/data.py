import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

def get_data():
    connection = psycopg2.connect(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        sslmode=os.getenv("DB_SSLMODE"),
    )

    cur = connection.cursor()
    cur.execute("SELECT * FROM bike_stations_status;")

    rows = cur.fetchall()
    colnames = [desc[0] for desc in cur.description]

    df = pd.DataFrame(rows, columns=colnames)

    cur.close()
    connection.close()
    return df


def get_data3():
    connection = psycopg2.connect(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        sslmode=os.getenv("DB_SSLMODE"),
    )

    cur = connection.cursor()
    cur.execute("SELECT * FROM bike_stations;")

    rows = cur.fetchall()
    colnames = [desc[0] for desc in cur.description]

    df = pd.DataFrame(rows, columns=colnames)

    cur.close()
    connection.close()
    return df



if __name__ == "__main__":
    df = get_data()
    df3=get_data3()
    print(df3.columns[df3.columns.duplicated()])

