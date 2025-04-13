import os
from typing import Any

from pymongo import MongoClient

client = MongoClient(os.getenv("MONGO_DB_URI"))
apdv_db = client["APDV"]
enterprises_collection = apdv_db["enterprises"]
enterprises_by_city_collection = apdv_db["enterprises_by_city"]
enterprises_by_country_collection = apdv_db["enterprises_by_country"]


def find_enterprises_by_country(county: str) -> list[Any]:
    return enterprises_by_country_collection.find({"country": county}).to_list()


def find_enterprises_by_city(city: str) -> list[Any]:
    return enterprises_by_city_collection.find({"city": city}).to_list()


def find_all() -> list[Any]:
    return enterprises_collection.find().to_list()

def find_enterprises_by_year(year) -> list[Any]:
    return enterprises_collection.find({"year": year}).to_list()

def find_enterprises_by_year_group_by_country(year):
    return enterprises_by_country_collection.find({"year": year}).to_list()

def find_enterprises_by_country_and_indic_ur(country, indic_ur):
    return enterprises_by_country_collection.find({"country": country, "indic_ur": indic_ur}).to_list()

def find_all_years():
    return list(enterprises_collection.find(filter={}, projection= {"year": 1}))


def find_all_by_country_year(year):
    return enterprises_by_country_collection.find({"year": year})

def find_all_enterprises_group_by_country():
    return enterprises_by_country_collection.find({})