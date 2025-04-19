import json

import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

from dagster import asset

from workflow.assets.sql_db_utils import get_engine


@asset(group_name="eu_enterprises")
def cities():
    url = 'https://db.nomics.world/Eurostat/urb_cecfi?tab=list'
    response = requests.get(url)
    parsed_data = BeautifulSoup(response.content, "html.parser")
    script_tags = parsed_data.find_all("script")
    for script in script_tags:
        if "dimensions_labels" in script.text:
            matched_string = re.search("dimensions_values_labels.*?,*freq", script.text, re.DOTALL)[0]
            city_mapping = matched_string.replace("dimensions_values_labels:{cities:", "").replace(",freq", "")
            cities = json.loads(city_mapping)
            cities = pd.DataFrame(cities)
            cities.columns = ["city", "city_name"]
            cities.to_sql('city_codes', get_engine(), if_exists='replace', index=False)
