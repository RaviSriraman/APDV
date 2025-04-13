from functools import cache
import pandas as pd
from models import enterprises
from models import country_codes

@cache
def find_all_enterprises() -> pd.DataFrame:
    return pd.DataFrame(enterprises.find_all())


@cache
def find_enterprises_by_city(city) -> pd.DataFrame:
    return pd.DataFrame(enterprises.find_enterprises_by_city(city))


@cache
def find_enterprises_by_country(country) -> pd.DataFrame:
    return pd.DataFrame(enterprises.find_enterprises_by_country(country))

@cache
def find_all_enterprises_group_by_country() -> pd.DataFrame:
    return pd.DataFrame(enterprises.find_all_enterprises_group_by_country())

@cache
def find_enterprises_by_year(year) -> pd.DataFrame:
    return pd.DataFrame(enterprises.find_enterprises_by_year(year))

@cache
def find_country_codes() -> pd.DataFrame:
    return pd.DataFrame(country_codes.find_country_codes())

@cache
def find_enterprises_by_country_and_indic_ur(country_value, indic_ur):
    return pd.DataFrame(enterprises.find_enterprises_by_country_and_indic_ur(country_value, indic_ur))

@cache
def find_all_years():
    return pd.DataFrame(enterprises.find_all_years())["year"].unique().astype(int).tolist()

@cache
def find_all_by_country_year(year):
    df = pd.DataFrame(enterprises.find_all_by_country_year(year))
    df = df.groupby(by=["country"]).agg({"enterprises": "sum", "c_enterprises": "sum"}).reset_index()
    return df

@cache
def find_enterprises_by_year_group_by_country(year) -> pd.DataFrame:
    return pd.DataFrame(enterprises.find_enterprises_by_year_group_by_country(year))