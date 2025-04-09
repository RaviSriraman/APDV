from functools import cache
import pandas as pd
from models import enterprises

@cache
def find_all_enterprises() -> pd.DataFrame:
    return pd.DataFrame(enterprises.find_all())


@cache
def find_enterprises_by_city(city) -> pd.DataFrame:
    return pd.DataFrame(enterprises.find_enterprises_by_city(city))


@cache
def find_enterprises_by_county(country) -> pd.DataFrame:
    return pd.DataFrame(enterprises.find_enterprises_by_county(country))