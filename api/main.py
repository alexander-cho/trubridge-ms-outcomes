import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from data.cdc_places import insert_cdc_data
from data.database import engine, wait_for_db

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
async def main():
    return {"message": "Hello from TruBridge MS Outcomes"}


# @app.get("/api/tracts")
# async def census_tract(state_abbr: str):
#     with Session(engine) as session:
#         statement = (
#             select(HealthOutcome.census_tract_id)
#             .where(HealthOutcome.state_abbr == state_abbr)
#             .distinct()
#         )
#
#         result = session.execute(statement)
#
#         tracts = result.scalars().all()
#
#     return tracts
