import os
from functools import cache
from io import StringIO
import re
import pandas as pd
import requests

from dagster import asset, AssetExecutionContext
from sqlalchemy import create_engine

from .constants import TOURISM_RAW_FILE_PATH


LOGGER_CONFIG = {"loggers": {"console": {"config": {"log_level": "INFO"}}}}

@cache
def get_engine():
    db_url = f"postgresql+psycopg2://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@{os.getenv("POSTGRES_HOST")}:5432/{os.getenv("POSTGRES_DB")}"
    return create_engine(db_url)


def remove_alphabets(value: str) -> str:
    if isinstance(value, str):
        result = re.findall(r'^[0-9]+', value)
        return result[0] if result else '0'
    return value

def read_http(http_url) -> pd.DataFrame:
    response = requests.get(http_url)
    content = response.text
    content = content.replace("\t", ",").replace(",:", ",0")
    return pd.read_csv(StringIO(content), delimiter=",")


@asset
def tours_file():
    df = read_http("https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/tour_dem_extot?format=TSV")
    df = df.rename(columns={"geo\\TIME_PERIOD": "geo"})
    df = df.drop("freq", axis=1)
    df_melted = df.melt(id_vars=['purpose', 'duration', 'c_dest', 'expend', 'statinfo', 'unit', 'geo'], var_name='year', value_name='amount')
    df_melted["amount"] = df_melted["amount"].apply(remove_alphabets)
    df_melted["year"] = pd.to_numeric(df_melted["year"].apply(lambda year: year.strip()))
    df_melted["amount"] = pd.to_numeric(df_melted["amount"])
    df_melted = df_melted[df_melted["amount"] != 0]
    df_melted.to_csv(TOURISM_RAW_FILE_PATH, index=False)


@asset(deps=["tours_file"])
def tours() -> None:
    df = pd.read_csv(TOURISM_RAW_FILE_PATH)
    df.to_sql('tours', get_engine(), if_exists='replace', index=False)


