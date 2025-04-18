import os
from functools import cache

import pandas as pd
from dagster import get_dagster_logger
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()


@cache
def get_engine():
    db_url = f"postgresql+psycopg2://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@{os.getenv("POSTGRES_HOST")}:5432/{os.getenv("POSTGRES_DB")}"
    return create_engine(db_url)


@cache
def fetch_tours_by_year(year) -> pd.DataFrame:
    try:
        return pd.read_sql(f"select * from tours where year={year}", con=get_engine())
    except:
        return pd.DataFrame([{}])


@cache
def find_city_codes() -> pd.DataFrame:
    try:
        return pd.read_sql("select * from city_codes", con=get_engine())
    except:
        return pd.DataFrame([{}])


def find_all_years() -> pd.DataFrame:
    try:
        return pd.read_sql("select year from tours", con=get_engine())['year'].unique()
    except:
        return pd.DataFrame([{}])


def find_all_destinations() -> pd.DataFrame:
    try:
        return pd.read_sql("select c_dest from tours", con=get_engine())["c_dest"].unique()
    except:
        return pd.DataFrame([{}])


def find_all_purposes() -> pd.DataFrame:
    try:
        return pd.read_sql("select purpose from tours", con=get_engine())["purpose"].unique()
    except:
        return pd.DataFrame([{}])

def fetch_tours_data_by_expenditure_destination_country(expenditure):
    try:
        return pd.read_sql(f"select * from tours_data_by_expenditure_destination_country where expenditure_and_investment = '{expenditure}'", con=get_engine())
    except:
        get_dagster_logger().debug("could not query mongo DB")
        return pd.DataFrame([{}])

def find_all_expenditures() -> list:
    try:
        return list(pd.read_sql("select distinct(expenditure_and_investment) from tours_data_by_expenditure_destination_country", con=get_engine())["expenditure_and_investment"].unique())
    except:
        get_dagster_logger().debug("could not query mongo DB")
        return []
