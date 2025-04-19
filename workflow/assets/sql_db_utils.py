from dagster import asset
from sqlalchemy import create_engine
import os
from functools import cache

@cache
def get_engine():
    db_url = f"postgresql+psycopg2://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@{os.getenv("POSTGRES_HOST")}:5432/{os.getenv("POSTGRES_DB")}"
    return create_engine(db_url)
