# import asyncio
import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from data.cdc_places import insert_cdc_data
from data.census import insert_vehicle_data, insert_internet_data, insert_insurance_data, insert_poverty_data
from data.db_engine import engine, wait_for_db
from schemas.tract import TractOut
from services.tracts import get_geometries, get_tract_data

load_dotenv()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    await wait_for_db(os.getenv('DB_CONNECTION_STRING'))

    # seed only if HealthOutcomes table is empty
    async with engine.connect() as conn:
        statement = await conn.execute(text("SELECT 1 FROM health_outcomes LIMIT 1;"))
        exists = statement.scalar_one_or_none() is not None

        if exists:
            pass
        else:
            await insert_cdc_data()
            await insert_vehicle_data()
            await insert_internet_data()
            await insert_poverty_data()
            await insert_insurance_data()

        await conn.execute(text("REFRESH MATERIALIZED VIEW tract_health_outcomes;"))
        await conn.execute(text("REFRESH MATERIALIZED VIEW tract_analytics;"))
        await conn.commit()

            # await asyncio.gather(
            #     insert_cdc_data(),
            #     insert_vehicle_data(),
            #     insert_internet_data()
            # )

    yield

    await engine.dispose()


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
async def census_tract(state_fp: str, tolerance: float):
    return await get_geometries(state_fp, tolerance)


@app.get("/api/tract")
async def get_tract_info(tract_id: str):
    return await get_tract_data(tract_id)
