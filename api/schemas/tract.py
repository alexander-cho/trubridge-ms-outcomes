from pydantic import BaseModel


class TractOut(BaseModel):
    geoid: str
    namelsad: str
    intptlat: str
    intptlon: str
    geom: dict
