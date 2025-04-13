from dagster import define_asset_job, AssetSelection, AssetsDefinition, AssetKey

all_jobs = define_asset_job(
    name="all_jobs",
    selection=AssetSelection.all()
)

enterprises_etl_job = define_asset_job(
    name="enterprises_etl_job",
    selection=AssetSelection.assets("enterprises_file", "enterprises", "enterprises_by_city", "enterprises_by_country")
)
