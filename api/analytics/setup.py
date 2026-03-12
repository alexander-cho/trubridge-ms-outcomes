# import polars as pl
from sqlalchemy import text

from data.db_engine import engine


async def get_feature_table():
    # df = pl.read_database(
    #     query="SELECT * FROM tract_analytics",
    #     connection=engine
    # )
    #
    # return df

    async with engine.connect() as conn:
        statement = await conn.execute(
            text("SELECT * FROM tract_analytics;")
        )

        res = statement.mappings().all()

    return res
