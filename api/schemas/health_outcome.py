from pydantic import BaseModel


class HealthOutcome(BaseModel):
    # id: int
    year: str
    state_abbr: str
    state_desc: str
    county_name: str
    county_fips: str
    data_source: str
    category: str
    measure: str
    data_value_unit: str
    data_value_type: str
    data_value: float
    low_confidence_limit: float
    high_confidence_limit: float
    total_population: int
    total_adult_population: int
    longitude: float
    latitude: float
    census_tract_id: str
    category_id: str
    measure_id: str
    data_value_type_id: str
    short_question_text: str
