import os
from typing import Any

from pymongo import MongoClient

client = MongoClient(os.getenv("MONGO_DB_URI"))
apdv_db = client["APDV"]

country_codes = apdv_db["country_codes"]


def find_country_codes() -> list[Any]:
    return country_codes.find().to_list()