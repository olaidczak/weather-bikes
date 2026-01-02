import os
from pathlib import Path
from dotenv import load_dotenv
import psycopg2

load_dotenv()

try:
    connection = psycopg2.connect(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        sslmode=os.getenv("DB_SSLMODE"),
    )

    cur = connection.cursor()

    ddl_path = Path(__file__).parent / "database.ddl"
    with open(ddl_path, "r") as f:
        ddl_script = f.read()

    cur.execute(ddl_script)
    connection.commit()
    print("Tables created successfully!")

except Exception as e:
    print(f"Error: {e}")

finally:
    if connection:
        cur.close()
        connection.close()
        print("PostgreSQL connection is closed")
