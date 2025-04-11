import os
from functools import cache

import pandas as pd
from sqlalchemy import create_engine

@cache
def get_engine():
    db_url = f"postgresql+psycopg2://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@{os.getenv("POSTGRES_HOST")}:5432/{os.getenv("POSTGRES_DB")}"
    return create_engine(db_url)

@cache
def fetch_by_year(year):
    with get_engine().connect() as conn:
        return pd.read_sql(f"select * from tours where year={year}", con=conn)