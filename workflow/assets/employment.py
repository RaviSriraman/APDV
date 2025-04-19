import pandas as pd
from dagster import asset, AssetExecutionContext

from .constants import EMPLOYMENTS_RAW_FILE_PATH


@asset(group_name="eu_employments")
def employments_file() -> None:
    df = pd.read_csv(
        "https://ec.europa.eu/eurostat/api/dissemination/sdmx/3.0/data/dataflow/ESTAT/tour_lfs1r2/1.0/*.*.*.*.*.*?c[freq]=A&c[nace_r2]=TOTAL,H51,I,I55,N79&c[wstatus]=EMP,SAL,SELF,CFAM,NRP&c[worktime]=TOTAL,PT,FT,NRP&c[unit]=THS_PER&c[geo]=EU27_2020,EA20,BE,BG,CZ,DK,DE,EE,IE,EL,ES,FR,HR,IT,CY,LV,LT,LU,HU,MT,NL,AT,PL,PT,RO,SI,SK,FI,SE,IS,NO,CH,UK,BA,ME,MK,RS,TR&c[TIME_PERIOD]=2024,2023,2022,2021,2020,2019,2018,2017,2016,2015,2014,2013,2012,2011,2010,2009,2008&compress=false&format=csvdata&formatVersion=2.0&lang=en&labels=name")

    df = df.rename(
        columns={"Geopolitical entity (reporting)": "country_name", "TIME_PERIOD": "year", "geo": "country_code",
                 "Statistical classification of economic activities in the European Community (NACE Rev. 2)": "work_field",
                 "Working time": "working_time", "OBS_VALUE": "employees_in_thousands"})

    df = df.drop(columns=["STRUCTURE", "STRUCTURE_ID", "STRUCTURE_NAME", "freq", "Time frequency", "nace_r2",
                          "Labour force and employment status", "Observation status (Flag) V2 structure", "CONF_STATUS",
                          "Confidentiality status (flag)", "unit", "Unit of measure", "worktime", "wstatus", "Time",
                           "Observation value", "OBS_FLAG"])
    df = df[~df["employees_in_thousands"].isna()]
    df = df[df["country_code"].str.len() < 3]
    df.to_csv(EMPLOYMENTS_RAW_FILE_PATH, index=False)


@asset(deps=["employments_file"], group_name="eu_employments", required_resource_keys={"mongo"})
def employments(context: AssetExecutionContext):
    df = pd.read_csv(EMPLOYMENTS_RAW_FILE_PATH)
    employments_df = df.reset_index().to_dict("records")
    employments_collection = context.resources.mongo["employments"]
    employments_collection.delete_many(filter={})
    employments_collection.insert_many(employments_df)


@asset(deps=["employments_file"], group_name="eu_employments", required_resource_keys={"mongo"})
def employments_by_working_time(context: AssetExecutionContext):
    df = pd.read_csv(EMPLOYMENTS_RAW_FILE_PATH)
    df = df.groupby(by=["year", "country_name", "country_code", "working_time"]).agg({"employees_in_thousands": "sum"}).reset_index()
    employments_df = df.reset_index().to_dict("records")
    employments_collection = context.resources.mongo["employments_by_working_time"]
    employments_collection.delete_many(filter={})
    employments_collection.insert_many(employments_df)


@asset(deps=["employments_file"], group_name="eu_employments", required_resource_keys={"mongo"})
def employments_by_work_field(context: AssetExecutionContext):
    df = pd.read_csv(EMPLOYMENTS_RAW_FILE_PATH)
    df = df.groupby(by=["year", "country_name", "country_code", "work_field"]).agg({"employees_in_thousands": "sum"}).reset_index()
    employments_df = df.reset_index().to_dict("records")
    employments_collection = context.resources.mongo["employments_by_work_field"]
    employments_collection.delete_many(filter={})
    employments_collection.insert_many(employments_df)