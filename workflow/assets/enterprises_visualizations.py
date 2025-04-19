
from dagster import file_relative_path, AssetExecutionContext

from dagstermill import define_dagstermill_asset
from dagster import asset, AssetIn, AssetKey
from sklearn import datasets
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from workflow.assets import constants

def find_enterprises(context):
    apdv_enterprises_collection = context.resources.mongo["enterprises"]
    enterprise = apdv_enterprises_collection.find()
    df = pd.DataFrame(enterprise)
    return df

# @asset(group_name="enterprises_visualizations")
def enterprises_dataset():
    sk_iris = datasets.load_iris()
    return pd.DataFrame(
        data=np.c_[sk_iris["data"], sk_iris["target"]],
        columns=sk_iris["feature_names"] + ["target"],
    )


# @asset(deps=["enterprises"], group_name="enterprises_visualizations", required_resource_keys={"mongo"})
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


# @asset(deps=["enterprises"], group_name="enterprises_visualizations", required_resource_keys={"mongo"})
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

# @asset(deps=["enterprises"], group_name="enterprises_visualizations", required_resource_keys={"mongo"})
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

# @asset(deps=["enterprises"], group_name="enterprises_visualizations", required_resource_keys={"mongo"})
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

# @asset(deps=["enterprises"], group_name="enterprises_visualizations", required_resource_keys={"mongo"})
def cities_distribution(context: AssetExecutionContext) -> None:
    df = find_enterprises(context)
    fig, ax = plt.subplots(figsize=(10, 10))
    df["city"].hist(bins=5, figsize=(20, 15))
    plt.savefig(constants.CITIES_HISTOGRAM_FILE_PATH, format="png", bbox_inches="tight")
    plt.close(fig)

# enterprises_visualization_notebook = define_dagstermill_asset(
#     name="enterprises_visualizations",
#     notebook_path = file_relative_path(__file__, "../../notebooks/enterprises-visualizations.ipynb"),
#     group_name="enterprises_visualizations",
#     ins={
#         "workflow": AssetIn(key=AssetKey("enterprises_dataset"))
#     }
# )