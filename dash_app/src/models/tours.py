import os

import pandas as pd
from sqlalchemy import create_engine

DB_URL = f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:5432/{os.getenv('POSTGRES_DB')}"
engine = create_engine(DB_URL)

def fetch_by_year(year):
    with engine.connect() as conn:
        return pd.read_sql(f"select * from tours where year={year}", con=conn)