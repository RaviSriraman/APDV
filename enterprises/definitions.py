from dagster import load_assets_from_modules, Definitions, file_relative_path
from dagstermill import ConfigurableLocalOutputNotebookIOManager

from .assets import enterprise, enterprises_visualizations
from .resources import mongo_resource
from .schedules import update_all_schedule

enterprise_assets = load_assets_from_modules([enterprise])
iris_assets = load_assets_from_modules([enterprises_visualizations])

defs = Definitions(
    assets=[*enterprise_assets, *iris_assets],
    resources={"mongo": mongo_resource, "output_notebook_io_manager": ConfigurableLocalOutputNotebookIOManager(base_dir=file_relative_path(__file__, "../notebooks/output"))},
    schedules=[update_all_schedule]
)
