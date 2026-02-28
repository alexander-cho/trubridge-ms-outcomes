import os
import time

from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()


# https://stackoverflow.com/questions/69381579/unable-to-start-fastapi-server-with-postgresql-using-docker-compose
def wait_for_db(db_uri):
    """checks if database connection is established"""

    _local_engine = create_engine(db_uri)

    up = False
    while not up:
        try:
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
        except Exception as err:
            print(f"Connection error: {err}")
            up = False
        else:
            up = True

        time.sleep(2)


engine = create_engine(os.getenv('DB_CONNECTION_STRING'))
