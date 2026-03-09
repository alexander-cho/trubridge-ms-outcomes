import os

import aiohttp
from dotenv import load_dotenv
import polars
from sqlalchemy import text
from pydantic import TypeAdapter

from data.db_engine import engine
from dtos.census_dtos import VehicleAvailabilityIn, InternetSubscriptionsIn, HealthInsuranceIn, PovertyIn

load_dotenv()


async def get_census_table(dataset, _get, _for, _in):
    """
    Query the Census API using a Census API key.
    :param dataset:
    :param _get:
    :param _for:
    :param _in:
    :return:
    """
    api_key = os.getenv('CENSUS_API_KEY')

    url = f"https://api.census.gov/data/{dataset}"

    params = {
        'get': _get,
        'for': _for,
        'in': _in,
        'key': api_key
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as res:
            parsed_data = await res.json()

    col_names, data = parsed_data[0], parsed_data[1:]

    df = polars.DataFrame(data=data, schema=col_names, orient="row")

    return df.write_json()


async def insert_vehicle_data():
    ct = await get_census_table('2024/acs/acs5','NAME,B08201_001E,B08201_002E,B08201_003E', 'tract:*', 'state:28')

    ta = TypeAdapter(list[VehicleAvailabilityIn])
    validated_ct = ta.validate_json(ct)

    insert_stmt = text("""
                       INSERT INTO vehicles_available (tract_name, total_households, total_households_no_vehicle, total_households_one_vehicle, tract_id)
                       VALUES (:tract_name, :total_households, :total_households_no_vehicle, :total_households_one_vehicle, :tract_id)
                       """)

    rows = [
        {
            "tract_name": obj.NAME,
            "total_households": obj.B08201_001E,
            "total_households_no_vehicle": obj.B08201_002E,
            "total_households_one_vehicle": obj.B08201_003E,
            "tract_id": obj.state + obj.county + obj.tract
        }
        for obj in validated_ct
    ]

    async with engine.begin() as conn:
        await conn.execute(insert_stmt, rows)


async def insert_internet_data():
    ct = await get_census_table('2024/acs/acs5', 'NAME,B28002_001E,B28002_013E', 'tract:*', 'state:28')

    ta = TypeAdapter(list[InternetSubscriptionsIn])
    validated_ct = ta.validate_json(ct)

    insert_stmt = text("""
                       INSERT INTO internet_subscriptions (tract_name, total_households,
                                                           total_households_no_internet_access, tract_id)
                       VALUES (:tract_name, :total_households, :total_households_no_internet_access, :tract_id)
                       """)

    rows = [
        {
            "tract_name": obj.NAME,
            "total_households": obj.B28002_001E,
            "total_households_no_internet_access": obj.B28002_013E,
            "tract_id": obj.state + obj.county + obj.tract
        }
        for obj in validated_ct
    ]

    async with engine.begin() as conn:
        await conn.execute(insert_stmt, rows)


async def insert_poverty_data():
    ct = await get_census_table('2024/acs/acs5', 'NAME,B17001_001E,B17001_002E', 'tract:*', 'state:28')

    ta = TypeAdapter(list[PovertyIn])
    validated_ct = ta.validate_json(ct)

    insert_stmt = text("""
                       INSERT INTO poverty (tract_name, total_population,
                                                           total_population_below_poverty_level, tract_id)
                       VALUES (:tract_name, :total_population, :total_population_below_poverty_level, :tract_id)
                       """)

    rows = [
        {
            "tract_name": obj.NAME,
            "total_population": obj.B17001_001E,
            "total_population_below_poverty_level": obj.B17001_002E,
            "tract_id": obj.state + obj.county + obj.tract
        }
        for obj in validated_ct
    ]

    async with engine.begin() as conn:
        await conn.execute(insert_stmt, rows)


async def insert_insurance_data():
    ct = await get_census_table('2024/acs/acs5/subject', 'NAME,S2701_C01_001E,S2701_C04_001E', 'tract:*', 'state:28')

    ta = TypeAdapter(list[HealthInsuranceIn])
    validated_ct = ta.validate_json(ct)

    insert_stmt = text("""
                       INSERT INTO health_insurance (tract_name, total_population,
                                                           total_population_uninsured, tract_id)
                       VALUES (:tract_name, :total_population, :total_population_uninsured, :tract_id)
                       """)

    rows = [
        {
            "tract_name": obj.NAME,
            "total_population": obj.S2701_C01_001E,
            "total_population_uninsured": obj.S2701_C04_001E,
            "tract_id": obj.state + obj.county + obj.tract
        }
        for obj in validated_ct
    ]

    async with engine.begin() as conn:
        await conn.execute(insert_stmt, rows)
