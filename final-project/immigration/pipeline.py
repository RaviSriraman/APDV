from typing import Any

import requests
from dagster import job, op, PythonObjectDagsterType
import pandas as pd

DataFrame = PythonObjectDagsterType(pd.DataFrame, name="PandasDataFrame")

@op
def fetch_local_authorities() -> Any:
    return requests.get("https://opendata.tailte.ie/api/Property/SearchLocalAuthority").json()

@op
def download_file(local_authorities):
    result = []
    for local_authority in local_authorities:
        url = f"https://opendata.tailte.ie/api/Property/GetProperties?Fields=*&Format=json&Download=false&LocalAuthority={local_authority['LaDesc']}"
        response = requests.get(url).content
        result.append(response)
        break
    return result

@job()
def immigration_pipeline():
    download_file(
        fetch_local_authorities()
    )