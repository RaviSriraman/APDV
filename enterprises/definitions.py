from dagster import load_assets_from_modules, Definitions

from .assets import enterprise
from .resources import mongo_resource
from .schedules import update_all_schedule

enterprise_assets = load_assets_from_modules([enterprise])

defs = Definitions(
    assets=enterprise_assets,
    resources={"mongo": mongo_resource},
    schedules=[update_all_schedule]
)
