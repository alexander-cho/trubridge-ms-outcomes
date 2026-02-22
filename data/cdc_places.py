import os
import requests
from dotenv import load_dotenv
from pydantic import ValidationError
from pydantic import TypeAdapter

from models.cdc_outcomes import CdcOutcome

load_dotenv()


def get_census_tract_data() -> list[CdcOutcome] | None:
    url = "https://data.cdc.gov/resource/cwsq-ngmh.json"
    params = {
        "$limit": 100,
        "$where": f"stateabbr = 'MS'"
    }
    headers = {
        "X-App-Token": os.getenv('SOCRATA_APP_TOKEN')
    }

    res = requests.get(url, params=params, headers=headers).json()

    try:
        ta = TypeAdapter(list[CdcOutcome])
        validated_res = ta.validate_python(res)
        return validated_res
    except ValidationError as e:
        print(e)
