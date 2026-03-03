from sqlalchemy import text

from data.db_engine import engine


def get_all_census_tracts(state_fp: str):
    with engine.connect() as connection:
        statement = connection.execute(
            text("SELECT * FROM ms_tracts WHERE statefp = :state_fp"),
            {"state_fp": state_fp}
        )

        tracts = statement.mappings().all()

    return tracts


def get_one_tract_info(tract_id: str):
    with engine.connect() as connection:
        statement = connection.execute(
            text("SELECT * FROM vehicles_available JOIN internet_subscriptions ON vehicles_available.tract_id = internet_subscriptions.tract_id"),
            {"tract_id": tract_id}
        )

        tract = statement.mappings().all()

    return tract
