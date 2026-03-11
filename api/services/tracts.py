from sqlalchemy import text

from data.db_engine import engine


async def get_geometries(state_fp: str, tolerance: float):
    """
    Get all tract geometries, for ex, default zoom at initial page load.
    :param tolerance:
    :param state_fp: the two-digit code to identify a U.S. state
    :return: geometries and supporting data on all tracts in a given state
    """
    async with engine.connect() as conn:
        statement = await conn.execute(
            text("SELECT * FROM "
                 "(SELECT geoid, namelsad, intptlat, intptlon, st_asgeojson(st_simplify(geom, (:tolerance)))::json as geom FROM ms_tracts WHERE statefp = :state_fp) "
                 "AS simplified WHERE geom IS NOT NULL;"),
            {"state_fp": state_fp, "tolerance": tolerance}
        )

        tracts = statement.mappings().all()

    return tracts


async def get_tract_data(tract_id: str):
    async with engine.connect() as conn:
        statement = await conn.execute(
            text(
                "SELECT * FROM tract_analytics WHERE census_tract_id = :tract_id;"),
            {"tract_id": tract_id}
        )

        tract = statement.mappings().all()

    return tract
