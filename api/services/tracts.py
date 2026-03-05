from sqlalchemy import text

from data.db_engine import engine


async def get_all_census_tracts(state_fp: str, tolerance: float):
    """
    Get all tracts, for ex, default zoom at initial page load.
    :param tolerance:
    :param state_fp: the two-digit code to identify a U.S. state
    :return: data on all tracts in a given state
    """
    async with engine.connect() as conn:
        statement = await conn.execute(
            text("SELECT * FROM "
                 "(SELECT geoid, namelsad, intptlat, intptlon, st_asgeojson(st_simplify(geom, (:tolerance)))::json as geom FROM ms_tracts WHERE statefp = :state_fp) "
                 "AS simplified WHERE geom IS NOT NULL"),
            {"state_fp": state_fp, "tolerance": tolerance}
        )

        tracts = statement.mappings().all()

    return tracts


async def get_one_tract_info(tract_id: str):
    async with engine.connect() as conn:
        statement = await conn.execute(
            text("SELECT * FROM vehicles_available JOIN internet_subscriptions ON vehicles_available.tract_id = internet_subscriptions.tract_id WHERE vehicles_available.tract_id = :tract_id"),
            {"tract_id": tract_id}
        )

        tract = statement.mappings().all()

    return tract
