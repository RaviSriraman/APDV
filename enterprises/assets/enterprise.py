import os
import re
from io import StringIO

import pandas as pd
import requests
import seaborn as sns
import matplotlib.pyplot as plt

from dagster import asset, AssetExecutionContext

from . import constants
from .constants import ENTERPRISES_RAW_FILE_PATH

LOGGER_CONFIG = {"loggers": {"console": {"config": {"log_level": "INFO"}}}}


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


@asset()
def enterprises_file() -> None:
    df = read_http("https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/urb_cecfi?format=TSV")
    df = df.rename(columns={"cities\\TIME_PERIOD": "city"})
    df = df.drop("freq", axis=1)
    df_melted = df.melt(id_vars=['indic_ur', 'city'], var_name='year', value_name='enterprises')
    df_melted["enterprises"] = df_melted["enterprises"].apply(remove_alphabets)
    df_melted["year"] = pd.to_numeric(df_melted["year"].apply(lambda year: year.strip()))
    df_melted["country"] = df_melted["city"].apply(lambda city: city[:2])
    df_melted = df_melted[df_melted["enterprises"] != "0"]
    df_melted["enterprises"] = pd.to_numeric(df_melted["enterprises"])
    df_melted.to_csv(ENTERPRISES_RAW_FILE_PATH, index=False)


@asset(deps=["enterprises_file"], required_resource_keys={"mongo"})
def enterprises(context) -> None:
    df = pd.read_csv(ENTERPRISES_RAW_FILE_PATH)
    enterprise = df.reset_index().to_dict("records")
    context.resources.mongo["enterprises"].insert_many(enterprise)


@asset(deps=["enterprises"], required_resource_keys={"mongo"})
def countries_with_most_enterprises(context: AssetExecutionContext) -> None:
    apdv_enterprises_collection = context.resources.mongo["enterprises"]
    enterprise = apdv_enterprises_collection.find()
    df = pd.DataFrame(enterprise)
    fig, ax = plt.subplots(figsize=(10, 10))
    countries_all_enterprises = df.groupby(by="country").agg({'enterprises': 'sum'})
    sns.barplot(countries_all_enterprises.sort_values(by="enterprises", ascending=False).head(10), x="country",
                y="enterprises").set_title("Countries with most")
    plt.savefig(constants.COUNTRIES_WITH_MOST_ENTERPRISES_FILE_PATH, format="png", bbox_inches="tight")
    plt.close(fig)


@asset(deps=["enterprises"], required_resource_keys={"mongo"})
def countries_with_least_enterprises(context: AssetExecutionContext) -> None:
    df = find_enterprises(context)
    fig, ax = plt.subplots(figsize=(10, 10))
    countries_all_enterprises = (df.groupby(by="country")
                                 .agg({'enterprises': 'sum'})
                                 .sort_values(by="enterprises", ascending=True).tail(10))
    (sns.barplot(countries_all_enterprises, x="country",y="enterprises")
     .set_title("Countries with least enterprises"))
    plt.savefig(constants.COUNTRIES_WITH_LEAST_ENTERPRISES_FILE_PATH, format="png", bbox_inches="tight")
    plt.close(fig)

@asset(deps=["enterprises"], required_resource_keys={"mongo"})
def cities_with_most_enterprises(context: AssetExecutionContext) -> None:
    df = find_enterprises(context)
    fig, ax = plt.subplots(figsize=(10, 10))
    countries_all_enterprises = (df.groupby(by="city")
                                 .agg({'enterprises': 'sum'})
                                 .sort_values(by="enterprises", ascending=False).tail(10))
    (sns.barplot(countries_all_enterprises, x="city",y="enterprises")
     .set_title("Cities with most enterprises"))
    plt.savefig(constants.CITIES_WITH_MOST_ENTERPRISES_FILE_PATH, format="png", bbox_inches="tight")
    plt.close(fig)

@asset(deps=["enterprises"], required_resource_keys={"mongo"})
def cities_with_least_enterprises(context: AssetExecutionContext) -> None:
    df = find_enterprises(context)
    fig, ax = plt.subplots(figsize=(10, 10))
    countries_all_enterprises = (df.groupby(by="city")
                                 .agg({'enterprises': 'sum'})
                                 .sort_values(by="enterprises", ascending=True).tail(10))
    (sns.barplot(countries_all_enterprises, x="city",y="enterprises")
     .set_title("Cities with least enterprises"))
    plt.savefig(constants.CITIES_WITH_LEAST_ENTERPRISES_FILE_PATH, format="png", bbox_inches="tight")
    plt.close(fig)

@asset(deps=["enterprises"], required_resource_keys={"mongo"})
def cities_distribution(context: AssetExecutionContext) -> None:
    df = find_enterprises(context)
    fig, ax = plt.subplots(figsize=(10, 10))
    df["city"].hist(bins=5, figsize=(20, 15))
    plt.savefig(constants.CITIES_HISTOGRAM_FILE_PATH, format="png", bbox_inches="tight")
    plt.close(fig)

def find_enterprises(context):
    apdv_enterprises_collection = context.resources.mongo["enterprises"]
    enterprise = apdv_enterprises_collection.find()
    df = pd.DataFrame(enterprise)
    return df
