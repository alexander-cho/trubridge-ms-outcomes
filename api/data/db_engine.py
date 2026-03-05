import asyncio
import os

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from dotenv import load_dotenv

load_dotenv()


# https://stackoverflow.com/questions/69381579/unable-to-start-fastapi-server-with-postgresql-using-docker-compose
async def wait_for_db(db_uri):
    """checks if database connection is established"""

    _local_engine = create_async_engine(db_uri)

    up = False
    while not up:
        try:
            async with _local_engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
        except Exception as err:
            print(f"Connection error: {err}")
            up = False
        else:
            up = True

        await asyncio.sleep(2)


engine = create_async_engine(os.getenv('DB_CONNECTION_STRING'))
