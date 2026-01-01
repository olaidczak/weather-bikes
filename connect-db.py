import os
from dotenv import load_dotenv
import psycopg2
load_dotenv()

try:
    # 1. Connect to the database
    connection = psycopg2.connect(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        sslmode=os.getenv("DB_SSLMODE")
    )

    # 2. Create a cursor object to execute queries
    cursor = connection.cursor()

    # 3. Execute a simple query
    cursor.execute("SELECT version();")

    # 4. Fetch the result
    record = cursor.fetchone()
    print("You are connected to - ", record)

except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL", error)

finally:
    # 5. Closing the connection
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")