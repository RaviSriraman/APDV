
from dagstermill import define_dagstermill_asset
from dagster import file_relative_path

from dagstermill import define_dagstermill_asset
from dagster import asset, AssetIn, AssetKey
from sklearn import datasets
import pandas as pd
import numpy as np


plotly_notebook = define_dagstermill_asset(
    name="dash_sample",
    notebook_path = file_relative_path(__file__, "../../notebooks/dash_example.ipynb"),
    group_name="plotly",
    ins={
    }
)