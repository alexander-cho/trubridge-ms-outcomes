import os

import requests
from dotenv import load_dotenv
import polars
from sqlalchemy import text
from pydantic import TypeAdapter

from data.db_engine import engine
from dtos.census_dtos import VehicleAvailabilityIn, InternetSubscriptionsIn

load_dotenv()


def get_census_table(_get, _for, _in):
    """
    Query the Census API using a Census API key.
    :param _get:
    :param _for:
    :param _in:
    :return:
    """
    api_key = os.getenv('CENSUS_API_KEY')

    url = f"https://api.census.gov/data/2024/acs/acs5"

    params = {
        'get': _get,
        'for': _for,
        'in': _in,
        'key': api_key
    }

    res = requests.get(url, params=params).json()

    col_names, data = res[0], res[1:]

    df = polars.DataFrame(data=data, schema=col_names, orient="row")

    return df.write_json()


def insert_vehicle_data():
    ct = get_census_table('NAME,B08201_001E,B08201_002E', 'tract:*', 'state:28')

    ta = TypeAdapter(list[VehicleAvailabilityIn])
    validated_ct = ta.validate_json(ct)

    insert_stmt = text("""
                       INSERT INTO vehicles_available (tract_name, total_households, total_households_no_vehicle, tract_id)
                       VALUES (:tract_name, :total_households, :total_households_no_vehicle, :tract_id)
                       """)

    with engine.connect() as connection:
        for obj in validated_ct:
            connection.execute(insert_stmt, {
                "tract_name": obj.NAME,
                "total_households": obj.B08201_001E,
                "total_households_no_vehicle": obj.B08201_002E,
                "tract_id": obj.state + obj.county + obj.tract
            })

        connection.commit()


def insert_internet_data():
    ct = get_census_table('NAME,B28002_001E,B28002_013E', 'tract:*', 'state:28')

    ta = TypeAdapter(list[InternetSubscriptionsIn])
    validated_ct = ta.validate_json(ct)

    insert_stmt = text("""
                       INSERT INTO internet_subscriptions (tract_name, total_households, total_households_no_internet_access, tract_id)
                       VALUES (:tract_name, :total_households, :total_households_no_internet_access, :tract_id)
                       """)

    with engine.connect() as connection:
        for obj in validated_ct:
            connection.execute(insert_stmt, {
                "tract_name": obj.NAME,
                "total_households": obj.B28002_001E,
                "total_households_no_internet_access": obj.B28002_013E,
                "tract_id": obj.state + obj.county + obj.tract
            })

        connection.commit()
