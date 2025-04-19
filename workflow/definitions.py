from dagster import load_assets_from_modules, Definitions, file_relative_path
from dagstermill import ConfigurableLocalOutputNotebookIOManager

from .assets import enterprise, enterprises_visualizations, country_codes, tourism, city_codes, tourism_enterprises, employment
from .resources import mongo_resource
from .schedules import enterprises_etl_job_schedule
from .jobs import apdv_etl_job

enterprise_assets = load_assets_from_modules([enterprise])
employment_assets = load_assets_from_modules([employment])
country_codes_assets = load_assets_from_modules([country_codes])
city_codes_assets = load_assets_from_modules([city_codes])
enterprises_visualizations_assets = load_assets_from_modules([enterprises_visualizations])
tourism_assets = load_assets_from_modules([tourism])
tourism_enterprises_assets = load_assets_from_modules([tourism_enterprises])

defs = Definitions(
    assets=[*enterprise_assets, *employment_assets, *enterprises_visualizations_assets, *country_codes_assets, *tourism_assets, *city_codes_assets, *tourism_enterprises_assets],
    resources={"mongo": mongo_resource, "output_notebook_io_manager": ConfigurableLocalOutputNotebookIOManager(base_dir=file_relative_path(__file__, "../notebooks/output"))},
    jobs=[apdv_etl_job],
    schedules=[enterprises_etl_job_schedule]
)
