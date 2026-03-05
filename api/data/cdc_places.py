import os

import aiohttp
from dotenv import load_dotenv
from pydantic import ValidationError, TypeAdapter
from sqlalchemy import text

from data.db_engine import engine
from dtos.cdc_outcomes import CdcPlacesOutcomeResponse

load_dotenv()


async def get_health_outcomes_data() -> list[CdcPlacesOutcomeResponse] | None:
    url = "https://data.cdc.gov/resource/cwsq-ngmh.json"
    params = {
        "$limit": 50000,
        "$where": f"stateabbr = 'MS'"
    }
    headers = {
        "X-App-Token": os.getenv('SOCRATA_APP_TOKEN')
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, headers=headers) as res:
            parsed_data = await res.json()

    try:
        ta = TypeAdapter(list[CdcPlacesOutcomeResponse])
        validated_res = ta.validate_python(parsed_data)
        return validated_res
    except ValidationError as e:
        print(e)
        return None


async def insert_cdc_data():
    health_outcomes_data = await get_health_outcomes_data()

    insert_stmt = text("""
                       INSERT INTO health_outcomes (year, state_abbr, state_desc, county_name, county_fips,
                                                    data_source, category, measure, data_value_unit, data_value_type,
                                                    data_value, low_confidence_limit, high_confidence_limit,
                                                    total_population, total_adult_population, longitude, latitude,
                                                    census_tract_id, category_id, measure_id, data_value_type_id,
                                                    short_question_text)
                       VALUES (:year, :state_abbr, :state_desc, :county_name, :county_fips,
                               :data_source, :category, :measure, :data_value_unit, :data_value_type,
                               :data_value, :low_confidence_limit, :high_confidence_limit,
                               :total_population, :total_adult_population, :longitude, :latitude,
                               :census_tract_id, :category_id, :measure_id, :data_value_type_id,
                               :short_question_text)
                       """)

    rows = [
        {
            "year": outcome.year,
            "state_abbr": outcome.stateabbr,
            "state_desc": outcome.statedesc,
            "county_name": outcome.countyname,
            "county_fips": outcome.countyfips,
            "data_source": outcome.datasource,
            "category": outcome.category,
            "measure": outcome.measure,
            "data_value_unit": outcome.data_value_unit,
            "data_value_type": outcome.data_value_type,
            "data_value": outcome.data_value,
            "low_confidence_limit": outcome.low_confidence_limit,
            "high_confidence_limit": outcome.high_confidence_limit,
            "total_population": outcome.totalpopulation,
            "total_adult_population": outcome.totalpop18plus,
            "longitude": outcome.geolocation.coordinates[0],
            "latitude": outcome.geolocation.coordinates[1],
            "census_tract_id": outcome.locationid,
            "category_id": outcome.categoryid,
            "measure_id": outcome.measureid,
            "data_value_type_id": outcome.datavaluetypeid,
            "short_question_text": outcome.short_question_text
        }
        for outcome in health_outcomes_data
    ]

    async with engine.connect() as conn:
        await conn.execute(insert_stmt, rows)
