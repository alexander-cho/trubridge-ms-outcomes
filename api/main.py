import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from data.cdc_places import insert_cdc_data
from data.census import insert_vehicle_data, insert_internet_data
from data.db_engine import engine, wait_for_db
from schemas.tract import TractOut
from services.tracts import get_all_census_tracts, get_one_tract_info

load_dotenv()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    wait_for_db(os.getenv('DB_CONNECTION_STRING'))

    # seed only if HealthOutcomes table is empty
    with engine.connect() as connection:
        statement = connection.execute(text("SELECT * FROM health_outcomes LIMIT 1"))
        exists = statement.scalar_one_or_none() is not None

        if exists:
            pass
        else:
            insert_cdc_data()
            insert_vehicle_data()
            insert_internet_data()

    yield


app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:5173",
    "https://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api")
def main():
    return {"message": "Hello from TruBridge MS Outcomes"}


@app.get("/api/tracts", response_model=list[TractOut])
def census_tract(state_fp: str, tolerance: float):
    return get_all_census_tracts(state_fp, tolerance)


@app.get("/api/tract")
def get_tract_info(tract_id: str):
    return get_one_tract_info(tract_id)
