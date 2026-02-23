import os

from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.getenv('DEV_DB_CONNECTION_STRING'))
