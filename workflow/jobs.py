from dagster import define_asset_job, AssetSelection, AssetsDefinition, AssetKey

apdv_etl_job = define_asset_job(
    name="apdv_etl_job",
    selection=AssetSelection.all()
)
