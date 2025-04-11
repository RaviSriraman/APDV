import os
from typing import Any

from pymongo import MongoClient

client = MongoClient(os.getenv("MONGO_DB_URI"))
apdv_db = client["APDV"]
enterprises_collection = apdv_db["enterprises"]


def find_enterprises_by_county(county: str) -> list[Any]:
    return enterprises_collection.find({"country": county}).to_list()


def find_enterprises_by_city(city: str) -> list[Any]:
    return enterprises_collection.find({"city": city}).to_list()


def find_all() -> list[Any]:
    return enterprises_collection.find().to_list()

def find_enterprises_by_year(year) -> list[Any]:
    return enterprises_collection.find({"year": year}).to_list()
