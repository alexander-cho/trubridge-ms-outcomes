from pydantic import BaseModel


class CdcPlacesOutcomeResponse(BaseModel):
    year: str
    stateabbr: str
    statedesc: str
    countyname: str
    countyfips: str
    locationname: str
    datasource: str
    category: str
    measure: str
    data_value_unit: str
    data_value_type: str
    data_value: float
    # data_value_footnote_symbol: str
    # data_value_footnote: str
    low_confidence_limit: float
    high_confidence_limit: float
    totalpopulation: int
    totalpop18plus: int
    geolocation: Geolocation
    locationid: str
    categoryid: str
    measureid: str
    datavaluetypeid: str
    short_question_text: str


class Geolocation(BaseModel):
    type: str
    coordinates: list


# class Coordinates(BaseModel):
#     longitude: float
#     latitude: float
