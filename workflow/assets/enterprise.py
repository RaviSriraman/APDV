import pandas as pd
from dagster import asset, AssetExecutionContext

from .constants import ENTERPRISES_RAW_FILE_PATH
from .utils import remove_alphabets, grouped_enterprises, read_http

LOGGER_CONFIG = {"loggers": {"console": {"config": {"log_level": "INFO"}}}}


@asset(group_name="eu_enterprises")
def enterprises_file() -> None:
    df = read_http("https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/urb_cecfi?format=TSV")
    df = df.rename(columns={"cities\\TIME_PERIOD": "city"})
    df = df.drop("freq", axis=1)
    df_melted = df.melt(id_vars=['indic_ur', 'city'], var_name='year', value_name='enterprises')
    df_melted["enterprises"] = df_melted["enterprises"].apply(remove_alphabets)
    df_melted["year"] = pd.to_numeric(df_melted["year"].apply(lambda year: year.strip()))
    df_melted["country"] = df_melted["city"].apply(lambda city: city[:2])
    df_melted["enterprises"] = pd.to_numeric(df_melted["enterprises"])
    df_melted.to_csv(ENTERPRISES_RAW_FILE_PATH, index=False)


@asset(deps=["enterprises_file"], group_name="eu_enterprises", required_resource_keys={"mongo"})
def enterprises(context: AssetExecutionContext) -> None:
    df = pd.read_csv(ENTERPRISES_RAW_FILE_PATH)
    enterprise = df.reset_index().to_dict("records")
    enterprises_collection = context.resources.mongo["enterprises"]
    enterprises_collection.delete_many(filter={})
    enterprises_collection.insert_many(enterprise)


@asset(deps=["enterprises"], group_name="eu_enterprises", required_resource_keys={"mongo"})
def enterprises_by_city(context: AssetExecutionContext):
    raw_df = pd.read_csv(ENTERPRISES_RAW_FILE_PATH)
    raw_df = raw_df.groupby(by=["indic_ur", "city", "year"]).agg({"enterprises": "sum"}).reset_index()
    ndf = raw_df[raw_df["enterprises"] != 0].groupby(by=["indic_ur", "city"]).agg(
        {"enterprises": "count"}).reset_index()
    ndf = ndf[ndf["enterprises"] > 11]
    raw_df = raw_df.merge(ndf, on=['city', 'indic_ur'])
    raw_df = raw_df.rename(columns={"enterprises_x": "enterprises"})
    grouped_enterprises(context, raw_df, "enterprises_by_city", ["indic_ur", "city"])


@asset(deps=["enterprises"], group_name="eu_enterprises", required_resource_keys={"mongo"})
def enterprises_by_country(context: AssetExecutionContext):
    raw_df = pd.read_csv(ENTERPRISES_RAW_FILE_PATH)
    raw_df = raw_df.groupby(by=["indic_ur", "country", "year"]).agg({"enterprises": "sum"}).reset_index()
    ndf = raw_df[raw_df["enterprises"] != 0].groupby(by=["indic_ur", "country"]).agg({"enterprises": "count"}).reset_index()
    ndf = ndf[ndf["enterprises"] > 11]
    raw_df = raw_df.merge(ndf, on=['country', 'indic_ur'])
    raw_df = raw_df.rename(columns={"enterprises_x": "enterprises"})
    grouped_enterprises(context, raw_df, "enterprises_by_country", ["indic_ur", "country"])
