from pydantic import BaseModel


class VehicleAvailabilityIn(BaseModel):
    NAME: str
    B08201_001E: str   # total
    B08201_002E: str   # total no vehicle
    state: str
    county: str
    tract: str


class InternetSubscriptionsIn(BaseModel):
    NAME: str
    B28002_001E: str   # total
    B28002_013E: str   # no internet access
    state: str
    county: str
    tract: str
