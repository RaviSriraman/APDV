from dagster import load_assets_from_modules, Definitions

from .assets import enterprises
from .resources import mongo_resource

enterprises_assets = load_assets_from_modules([enterprises])

defs = Definitions(
    assets=enterprises_assets,
    resources={"mongo": mongo_resource}
)