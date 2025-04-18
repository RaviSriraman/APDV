import os

import pandas as pd
from pymongo import MongoClient

from utils.sql_db_utils import get_engine

client = MongoClient(os.getenv("MONGO_DB_URI"))
apdv_db = client["APDV"]
tours_collection = apdv_db["tours"]
tours_by_purpose_destination_country_collection = apdv_db["tours_by_purpose_destination_country"]
tours_data_by_expenditure_destination_country_collection = apdv_db["tours_data_by_expenditure_destination_country"]
tours_by_purpose_source_country_collection = apdv_db["tours_by_purpose_source_country"]


def fetch_by_year(year):
    return pd.read_sql(f"select * from tours where year={year}", con=get_engine())


def fetch_domestic_tours_by_country_all_purpose_enterprises(year):
    return pd.read_sql(
        f"""SELECT country, year, country_name, amount, indic_ur, enterprises, ma_enterprises, c_enterprises 
        FROM domestic_tours_by_country_all_purpose_enterprises where 
        c_enterprises is not null and year={year} """
        , con=get_engine())


def fetch_domestic_tours_by_country_all_purpose_enterprises_by_country(country):
    return pd.read_sql(
        f"""SELECT country, year, country_name, amount, indic_ur, enterprises, ma_enterprises, c_enterprises 
        FROM domestic_tours_by_country_all_purpose_enterprises where 
        c_enterprises is not null and country_name='{country}' """, con=get_engine())


def find_tours_by_purpose_destination_country(purpose):
    return list(tours_by_purpose_destination_country_collection.find({"Purpose": purpose}))


def fetch_all_purposes():
    return list(tours_collection.find(filter={}, projection={"Purpose": 1}))


def fetch_all_years():
    return list(tours_collection.find(filter={}, projection={"year": 1}))


def find_tours_by_purpose_destination_country_year(year):
    return list(tours_by_purpose_destination_country_collection.find({"year": year}))


def find_tours_data_by_expenditure_destination_country(expenditure):
    return list(tours_data_by_expenditure_destination_country_collection.find({"expenditure_and_investment": expenditure}))

def find_all_expenditures():
    return tours_data_by_expenditure_destination_country_collection.find(filter={}, projection={"expenditure_and_investment": 1})