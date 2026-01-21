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
    # query = """
    #     SELECT
    #     batch_id,
    #     ROUND(
    #         (SUM(free_bikes + empty_slots) - SUM(free_bikes))/(SUM(free_bikes + empty_slots)),
    #         4
    #     ) AS used_bikes
    #     FROM bike_stations_status
    #     GROUP BY batch_id
    #     ORDER BY batch_id;
    # """

    query = """
        SELECT
            bss.batch_id,
            bss.used_bikes,
            wd.*
        FROM (
            SELECT
                batch_id,
                ROUND(
                    (SUM(free_bikes + empty_slots) - SUM(free_bikes))::numeric / 
                    (SUM(free_bikes + empty_slots))::numeric,
                    4
                ) AS used_bikes
            FROM bike_stations_status
            GROUP BY batch_id
        ) bss
        JOIN weather_data wd ON bss.batch_id = wd.batch_id
        ORDER BY bss.batch_id;
    """

    cur.execute(query)

    rows = cur.fetchall()
    colnames = [desc[0] for desc in cur.description]

    df = pd.DataFrame(rows, columns=colnames)

    cur.close()
    connection.close()
    return df
