from io import StringIO

import numpy as np
import re

import requests
import pandas as pd


def read_http(http_url) -> pd.DataFrame:
    response = requests.get(http_url)
    content = response.text
    content = content.replace("\t", ",").replace(",:", ",0")
    return pd.read_csv(StringIO(content), delimiter=",")

def merge_calculated_and_original_counts(enterprise_df):
    return enterprise_df["ma_enterprises"] if enterprise_df["enterprises"] == 0 else enterprise_df["enterprises"]

def grouped_enterprises(context, raw_df, collection_name, by):
    collection = context.resources.mongo[collection_name]
    collection.delete_many(filter={})
    for _, df in raw_df.groupby(by=by):
        df["enterprises"] = pd.to_numeric(df["enterprises"])
        df["ma_enterprises"] = df["enterprises"].replace(0, np.nan).ffill().bfill()[::-1].rolling(3, 1).mean().astype(int)
        df["c_enterprises"] = df.apply(merge_calculated_and_original_counts, axis=1)
        enterprise = df.reset_index().to_dict("records")
        collection.insert_many(enterprise)

def remove_alphabets(value: str) -> str:
    if isinstance(value, str):
        result = re.findall(r'^[0-9]+', value)
        return result[0] if result else '0'
    return value