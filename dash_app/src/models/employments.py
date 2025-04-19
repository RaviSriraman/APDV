import os
from typing import Any

from pymongo import MongoClient

client = MongoClient(os.getenv("MONGO_DB_URI"))
apdv_db = client["APDV"]
employments_collection = apdv_db["employments"]
employments_by_working_time_collection = apdv_db["employments_by_working_time"]
employments_by_work_field_collection = apdv_db["employments_by_work_field"]


def find_employments_by_working_time(working_time: str) -> list[Any]:
    return employments_by_working_time_collection.find({"working_time": working_time}).to_list()


def find_employments_by_work_field(work_field: str) -> list[Any]:
    return employments_by_work_field_collection.find({"work_field": work_field}).to_list()

def find_all_employments() -> list[Any]:
    return employments_collection.find({}).to_list()

def find_all_work_fields():
    return list(employments_by_work_field_collection.find(filter={}, projection={"work_field": 1}))

def find_all_working_times():
    return list(employments_by_working_time_collection.find(filter={}, projection={"working_time": 1}))


def find_employments_by_year(year):
    return list(employments_by_work_field_collection.find({"year": year}))


def find_all_years():
    return list(employments_by_work_field_collection.find(filter={}, projection={"year": 1}))