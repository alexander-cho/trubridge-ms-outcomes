from sqlalchemy import text

from data.database import engine


async def get_all_census_tracts(state_abbr: str):
    with engine.connect() as connection:
        statement = connection.execute(
            text("SELECT DISTINCT census_tract_id FROM health_outcomes WHERE state_abbr = :state_abbr"),
            {"state_abbr": state_abbr}
        )

        tracts = statement.scalars().all()

    return tracts
