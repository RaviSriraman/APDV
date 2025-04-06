import os

from dagster import resource
from pymongo import MongoClient


@resource
def mongo_resource():
    """Return a MongoDB client instance."""
    uri = os.getenv("MONGO_DB_URI")
    print(uri)
    return MongoClient(uri)["APDV"]
