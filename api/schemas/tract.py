from pydantic import BaseModel


# use actual type
class Geometry:
    pass


class Tract(BaseModel):
    # gid: int
    statefp: str
    countyfp: str
    tractce: str
    geoid: str
    geoidfq: str
    name: str
    namelsad: str
    mtfcc: str
    funcstat: str
    aland: float
    awater: float
    intptlat: str
    intptlon: str
    geom: Geometry
