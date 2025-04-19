from functools import cache
import pandas as pd
from dagster import get_dagster_logger

from models import enterprises, country_codes, employments, tours

def fetch_tours_by_purpose_destination_country(purpose) -> pd.DataFrame:
    try:
        return pd.DataFrame(tours.find_tours_by_purpose_destination_country(purpose))
    except:
        get_dagster_logger().debug("could not query mongo DB")
        return pd.DataFrame([{}])


def fetch_all_tour_purposes():
    return list(pd.DataFrame(tours.fetch_all_purposes())["Purpose"].unique())


def fetch_all_tour_years():
    return list(pd.DataFrame(tours.fetch_all_years())["year"].unique())


def fetch_tours_by_purpose_destination_year(year) -> pd.DataFrame:
    try:
        return pd.DataFrame(tours.find_tours_by_purpose_destination_country_year(year))
    except:
        get_dagster_logger().debug("could not query mongo DB")
        return pd.DataFrame([{}])


def fetch_tours_data_by_expenditure_destination_country(expenditure):
    try:
        return pd.DataFrame(tours.find_tours_data_by_expenditure_destination_country(expenditure))
    except:
        get_dagster_logger().debug("could not query mongo DB")
        return pd.DataFrame([{}])

def find_all_expenditures() -> list:
    try:
        return list(pd.DataFrame(tours.find_all_expenditures())["expenditure_and_investment"].unique())
    except:
        get_dagster_logger().debug("could not query mongo DB")
        return []

@cache
def find_all_enterprises() -> pd.DataFrame:
    try:
        return pd.DataFrame(enterprises.find_all())
    except:
        get_dagster_logger().debug("could not query data from mongoDB")
        return pd.DataFrame([{}])


@cache
def find_enterprises_by_city(city) -> pd.DataFrame:
    try:
        return pd.DataFrame(enterprises.find_enterprises_by_city(city))
    except:
        get_dagster_logger().debug("could not query data from mongoDB")
        return pd.DataFrame([{}])


@cache
def find_all_enterprises_by_city() -> pd.DataFrame:
    try:
        return pd.DataFrame(enterprises.find_all_enterprises_by_city())
    except:
        get_dagster_logger().debug("could not query data from mongoDB")
        return pd.DataFrame([{}])


@cache
def find_enterprises_by_country(country) -> pd.DataFrame:
    try:
        return pd.DataFrame(enterprises.find_enterprises_by_country(country))
    except:
        get_dagster_logger().debug("could not query data from mongoDB")
        return pd.DataFrame([{}])


@cache
def find_all_enterprises_group_by_country() -> pd.DataFrame:
    try:
        return pd.DataFrame(enterprises.find_all_enterprises_group_by_country())
    except:
        get_dagster_logger().debug("could not query data from mongoDB")
        return pd.DataFrame([{}])


@cache
def find_enterprises_by_year(year) -> pd.DataFrame:
    try:
        return pd.DataFrame(enterprises.find_enterprises_by_year(year))
    except:
        get_dagster_logger().debug("could not query data from mongoDB")
        return pd.DataFrame({})


@cache
def find_country_codes() -> pd.DataFrame:
    try:
        return pd.DataFrame(country_codes.find_country_codes())
    except:
        get_dagster_logger().debug("could not query data from mongoDB")
        return pd.DataFrame([{}])


@cache
def find_enterprises_by_country_and_indic_ur(country_value, indic_ur):
    try:
        return pd.DataFrame(enterprises.find_enterprises_by_country_and_indic_ur(country_value, indic_ur))
    except:
        get_dagster_logger().debug("could not query data from mongoDB")
        return pd.DataFrame([{}])


@cache
def find_all_years():
    try:
        return pd.DataFrame(enterprises.find_all_years())["year"].unique().astype(int).tolist()
    except:
        get_dagster_logger().debug("could not query data from mongoDB")
        return pd.DataFrame([{}])


@cache
def find_all_by_country_year(year):
    try:
        df = pd.DataFrame(enterprises.find_all_by_country_year(year))
        df = df.groupby(by=["country"]).agg({"enterprises": "sum", "c_enterprises": "sum"}).reset_index()
        return df
    except:
        get_dagster_logger().debug("could not query data from mongoDB")
        return pd.DataFrame([{}])


@cache
def find_enterprises_by_year_group_by_country(year) -> pd.DataFrame:
    try:
        return pd.DataFrame(enterprises.find_enterprises_by_year_group_by_country(year))
    except:
        get_dagster_logger().debug("could not query data from mongoDB")
        return pd.DataFrame([{}])


def find_employments_by_working_time(working_time: str) -> pd.DataFrame:
    try:
        return pd.DataFrame(employments.find_employments_by_working_time(working_time))
    except:
        get_dagster_logger().debug("could not query data from mongoDB")
        return pd.DataFrame([{}])


def find_employments_by_work_field(work_field: str) -> pd.DataFrame:
    try:
        return pd.DataFrame(employments.find_employments_by_work_field(work_field))
    except:
        get_dagster_logger().debug("could not query data from mongoDB")
        return pd.DataFrame([{}])


def find_all_employments() -> pd.DataFrame:
    try:
        return pd.DataFrame(employments.find_all_employments())
    except:
        get_dagster_logger().debug("could not query data from mongoDB")
        return pd.DataFrame([{}])


def find_all_work_fields() -> list[str]:
    try:
        return list(pd.DataFrame(employments.find_all_work_fields())["work_field"].unique())
    except :
        get_dagster_logger().debug("could not query data from mongoDB")
        return []

def find_all_working_times() -> list[str]:
    try:
        return list(pd.DataFrame(employments.find_all_working_times())["working_time"].unique())
    except:
        get_dagster_logger().debug("could not query data from mongoDB")
        return []


def find_employments_by_year(year) -> pd.DataFrame:
    try:
        return pd.DataFrame(employments.find_employments_by_year(year))
    except:
        get_dagster_logger().debug("could not query data from mongoDB")
        return pd.DataFrame([{}])


def find_all_years_from_employments() -> list[int]:
    try:
        return list(pd.DataFrame(employments.find_all_years())["year"].astype(int).unique())
    except:
        get_dagster_logger().debug("could not query data from mongoDB")
        return []

