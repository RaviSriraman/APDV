
from dagstermill import define_dagstermill_asset
from dagster import file_relative_path

from dagstermill import define_dagstermill_asset
from dagster import asset, AssetIn, AssetKey
from sklearn import datasets
import pandas as pd
import numpy as np

@asset
def enterprises_dataset():
    sk_iris = datasets.load_iris()
    return pd.DataFrame(
        data=np.c_[sk_iris["data"], sk_iris["target"]],
        columns=sk_iris["feature_names"] + ["target"],
    )

enterprises_visualization_notebook = define_dagstermill_asset(
    name="enterprises_visualizations",
    notebook_path = file_relative_path(__file__, "../../notebooks/enterprises-visualizations.ipynb"),
    group_name="workflow",
    ins={
        "workflow": AssetIn(key=AssetKey("enterprises_dataset"))
    }
)