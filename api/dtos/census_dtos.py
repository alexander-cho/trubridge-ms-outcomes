from pydantic import BaseModel


class VehicleAvailabilityIn(BaseModel):
    NAME: str
    B08201_001E: str   # total households
    B08201_002E: str   # total households no vehicle
    B08201_003E: str   # total households 1 vehicle available
    state: str
    county: str
    tract: str


class InternetSubscriptionsIn(BaseModel):
    NAME: str
    B28002_001E: str   # total households
    B28002_013E: str   # total households no internet access
    state: str
    county: str
    tract: str


class PovertyIn(BaseModel):
    NAME: str
    B17001_001E: str   # total population
    B17001_002E: str   # total population income below poverty level
    state: str
    county: str
    tract: str


class HealthInsuranceIn(BaseModel):
    NAME: str
    S2701_C01_001E: str   # total population
    S2701_C04_001E: str   # total population uninsured
    state: str
    county: str
    tract: str
