import re
from io import StringIO

import pandas as pd
import requests
import seaborn as sns
import matplotlib.pyplot as plt

from dagster import asset

from . import constants
from .constants import ENTERPRISES_RAW_FILE_PATH


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
    enterprises = df.reset_index().to_dict("records")
    context.resources.mongo["enterprises"].insert_many(enterprises)


@asset(deps=["enterprises"], required_resource_keys={"mongo"})
def top_economic_countries(context) -> None:
    apdv_enterprises_collection = context.resources.mongo["enterprises"]
    enterprises = apdv_enterprises_collection.find()
    df = pd.DataFrame(enterprises)
    fig, ax = plt.subplots(figsize=(10, 10))
    countries_all_enterprises = df[(df["year"] == 1998)].groupby(by="country").agg({'enterprises': 'sum'})
    sns.barplot(countries_all_enterprises.sort_values(by="enterprises", ascending=True).tail(10)[::-1], x="country",
                y="enterprises").set_title("Number of enterprises in top european countries in 1998")
    plt.savefig(constants.TOP_ECONOMIC_FILE_PATH, format="png", bbox_inches="tight")
    plt.close(fig)
