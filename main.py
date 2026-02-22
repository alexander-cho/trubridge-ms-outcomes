from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from data.cdc_places import get_census_tract_data

app = FastAPI()


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


@app.get("/")
async def main():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/cdc-places")
async def census_tract():
    return get_census_tract_data()
