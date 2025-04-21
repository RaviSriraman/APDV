import pandas as pd

from dagster import asset, AssetExecutionContext

from .constants import TOURISM_RAW_FILE_PATH, TOURISM_RAW_CSV_FILE_PATH
from .enterprise import read_http
from .sql_db_utils import get_engine
from .utils import remove_alphabets

LOGGER_CONFIG = {"loggers": {"console": {"config": {"log_level": "INFO"}}}}


@asset(group_name="eu_tourism")
def tours_file():
    df = read_http("https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/tour_dem_extot?format=TSV")
    df = df.rename(columns={"geo\\TIME_PERIOD": "country"})
    df = df.drop("freq", axis=1)
    df_melted = df.melt(id_vars=['purpose', 'duration', 'c_dest', 'expend', 'statinfo', 'unit', 'country'], var_name='year', value_name='amount')
    df_melted["amount"] = df_melted["amount"].apply(remove_alphabets)
    df_melted["year"] = pd.to_numeric(df_melted["year"].apply(lambda year: year.strip()))
    df_melted["amount"] = pd.to_numeric(df_melted["amount"])
    df_melted.to_csv(TOURISM_RAW_FILE_PATH, index=False)


@asset(deps=["tours_file"], group_name="eu_tourism")
def tours() -> None:
    df = pd.read_csv(TOURISM_RAW_FILE_PATH)
    df.to_sql('tours', get_engine(), if_exists='replace', index=False)


@asset(deps=["tours_file"], group_name="eu_tourism")
def tours_by_country_all_purpose() -> None:
    df = pd.read_csv(TOURISM_RAW_FILE_PATH)
    df = df.groupby(by=["country", "year"]).agg({"amount": "sum"}).reset_index()
    df.to_sql('tours_by_country_all_purpose', get_engine(), if_exists='replace', index=False)


@asset(group_name="eu_tourism")
def tours_csv_file() -> None:
    df = pd.read_csv(
        "https://ec.europa.eu/eurostat/api/dissemination/sdmx/3.0/data/dataflow/ESTAT/tour_dem_extotw/1.0/*.*.*.*.*.*.*.*?c[freq]=A&c[purpose]=PER,PROF&c[duration]=N_GE1,N1-3,N_GE4&c[c_dest]=BE,DK,DE,EL,ES,FR,HR,IT,LU,NL,AT,PL,PT,RO,SI,FI,SE,IS,NO,CH,UK&c[expend]=TOTXDUR,TRA,REST,ACCOM,TRP_OTH,DUR,PACK_ARR&c[statinfo]=AVG_TRP,AVG_NGT&c[unit]=EUR&c[geo]=BE,BG,CZ,DK,DE,EE,IE,EL,ES,FR,HR,IT,CY,LV,LT,LU,HU,MT,NL,AT,PL,PT,RO,SI,SK,FI,SE,NO,CH,UK,ME,MK,AL,RS&c[TIME_PERIOD]=2023,2022,2021,2020,2019,2018,2017,2016,2015,2014,2013,2012&compress=false&format=csvdata&formatVersion=2.0&lang=en&labels=name")
    df = df.drop(columns=["STRUCTURE", "STRUCTURE_ID", "STRUCTURE_NAME", "freq", "Time frequency", "Observation value",
                          "OBS_FLAG", "Observation status (Flag) V2 structure", "CONF_STATUS",
                          "Confidentiality status (flag)", "Time", "unit", "Unit of measure"])

    df = df.rename(columns={"geo": "country", "OBS_VALUE": "amount", "TIME_PERIOD": "year",
                            "Country of destination": "destination_country",
                            "Geopolitical entity (reporting)": "country_name",
                            "Expenditure and investment": "expenditure_and_investment"})

    df.to_csv(TOURISM_RAW_CSV_FILE_PATH)

@asset(deps=["tours_csv_file"], group_name="eu_tourism", required_resource_keys={"mongo"})
def tours_data(context: AssetExecutionContext):
    tours = pd.read_csv(TOURISM_RAW_CSV_FILE_PATH).to_dict(orient="records")
    employments_collection = context.resources.mongo["tours"]
    employments_collection.delete_many(filter={})
    employments_collection.insert_many(tours)


@asset(deps=["tours_csv_file", "country_codes"], group_name="eu_tourism")
def domestic_tours_by_country_all_purpose() -> None:
    df = pd.read_csv(TOURISM_RAW_CSV_FILE_PATH)
    combined_df = df.groupby(by=["country", "year", "country_name"]).agg({"amount": "sum"}).reset_index()
    combined_df.to_sql('domestic_tours_by_country_all_purpose', get_engine(), if_exists='replace', index=False)


@asset(deps=["tours_csv_file"], group_name="eu_tourism", required_resource_keys={"mongo"})
def tours_data_by_purpose_source_country(context: AssetExecutionContext):
    df = pd.read_csv(TOURISM_RAW_CSV_FILE_PATH).groupby(by=["purpose", "Purpose", "country", "country_name", "year"]).agg({"amount": "sum"}).reset_index()
    tours = df.to_dict(orient="records")
    employments_collection = context.resources.mongo["tours_by_purpose_source_country"]
    employments_collection.delete_many(filter={})
    employments_collection.insert_many(tours)


@asset(deps=["tours_csv_file"], group_name="eu_tourism", required_resource_keys={"mongo"})
def tours_data_by_purpose_destination_country(context: AssetExecutionContext):
    df = pd.read_csv(TOURISM_RAW_CSV_FILE_PATH).groupby(by=["purpose", "Purpose", "c_dest", "destination_country", "year"]).agg({"amount": "sum"}).reset_index()
    tours = df.to_dict(orient="records")
    employments_collection = context.resources.mongo["tours_by_purpose_destination_country"]
    employments_collection.delete_many(filter={})
    employments_collection.insert_many(tours)


@asset(deps=["tours_csv_file"], group_name="eu_tourism", required_resource_keys={"mongo"})
def tours_data_by_expenditure_destination_country(context: AssetExecutionContext):
    df = pd.read_csv(TOURISM_RAW_CSV_FILE_PATH).groupby(by=["expend", "expenditure_and_investment", "country", "country_name", "year"]).agg({"amount": "sum"}).reset_index()
    tours_expenditure = df.to_dict(orient="records")
    employments_collection = context.resources.mongo["tours_data_by_expenditure_destination_country"]
    employments_collection.delete_many(filter={})
    employments_collection.insert_many(tours_expenditure)


@asset(deps=["tours_csv_file"], group_name="eu_tourism", required_resource_keys={"mongo"})
def tours_data_by_purpose_destination_country_postgres():
    df = pd.read_csv(TOURISM_RAW_CSV_FILE_PATH).groupby(
        by=["purpose", "Purpose", "c_dest", "destination_country", "year"]).agg({"amount": "sum"}).reset_index()
    df.to_sql("tours_data_by_purpose_destination_country", con=get_engine(), if_exists="replace", index=False)


@asset(deps=["tours_csv_file"], group_name="eu_tourism")
def tours_data_by_expenditure_destination_country_postgres():
    df = pd.read_csv(TOURISM_RAW_CSV_FILE_PATH).groupby(
        by=["expend", "expenditure_and_investment", "country", "country_name", "year"]).agg(
        {"amount": "sum"}).reset_index()
    df.to_sql("tours_data_by_expenditure_destination_country", con=get_engine(), if_exists="replace", index=False)