from dagster import define_asset_job, AssetSelection

all_jobs = define_asset_job(
    name="all_jobs",
    selection=AssetSelection.all()
)
