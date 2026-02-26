import os
import requests
from dotenv import load_dotenv
from pydantic import ValidationError
from pydantic import TypeAdapter
from sqlalchemy.orm import Session

from data.database import engine
from models.health_outcome import HealthOutcome
from schemas.cdc_outcomes import CdcPlacesOutcomeResponse

load_dotenv()


def get_census_tract_data() -> list[CdcPlacesOutcomeResponse] | None:
    url = "https://data.cdc.gov/resource/cwsq-ngmh.json"
    params = {
        "$limit": 50000,
        "$where": f"stateabbr = 'MS'"
    }
    headers = {
        "X-App-Token": os.getenv('SOCRATA_APP_TOKEN')
    }

    res = requests.get(url, params=params, headers=headers).json()

    try:
        ta = TypeAdapter(list[CdcPlacesOutcomeResponse])
        validated_res = ta.validate_python(res)
        return validated_res
    except ValidationError as e:
        print(e)


def insert_cdc_data():
    census_tract_data = get_census_tract_data()
    with Session(engine) as session:
        for outcome in census_tract_data:
            health_outcome = HealthOutcome(
                year = outcome.year,
                state_abbr = outcome.stateabbr,
                state_desc = outcome.statedesc,
                county_name = outcome.countyname,
                county_fips = outcome.countyfips,
                data_source = outcome.datasource,
                category = outcome.category,
                measure = outcome.measure,
                data_value_unit = outcome.data_value_unit,
                data_value_type = outcome.data_value_type,
                data_value = outcome.data_value,
                low_confidence_limit = outcome.low_confidence_limit,
                high_confidence_limit = outcome.high_confidence_limit,
                total_population = outcome.totalpopulation,
                total_adult_population = outcome.totalpop18plus,
                longitude = outcome.geolocation.coordinates[0],
                latitude = outcome.geolocation.coordinates[1],
                census_tract_id = outcome.locationid,
                category_id = outcome.categoryid,
                measure_id = outcome.measureid,
                data_value_type_id = outcome.datavaluetypeid,
                short_question_text = outcome.short_question_text,
            )

            session.add(health_outcome)
            session.commit()
