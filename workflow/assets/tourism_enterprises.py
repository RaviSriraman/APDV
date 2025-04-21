from dagster import asset, AssetExecutionContext
import pandas as pd

from workflow.assets.sql_db_utils import get_engine

@asset(deps=["domestic_tours_by_country_all_purpose", "enterprises_by_country"], group_name="eu_enterprises_tourism", required_resource_keys={"mongo"})
def domestic_tours_by_country_all_purpose_enterprises(context: AssetExecutionContext):
    df = pd.DataFrame(context.resources.mongo["enterprises_by_country"].find({}))
    domestic_tours_df = pd.read_sql("select * from domestic_tours_by_country_all_purpose", con=get_engine())
    domestic_tours_by_country_all_purpose_enterprises_df = pd.merge(domestic_tours_df, df, on=["country", "year"], how="left")
    domestic_tours_by_country_all_purpose_enterprises_df.drop(axis=1, columns=["_id", "index"], inplace=True)
    domestic_tours_by_country_all_purpose_enterprises_df.to_sql("domestic_tours_by_country_all_purpose_enterprises", con=get_engine(), index=False, if_exists="replace")