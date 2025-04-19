import requests
from bs4 import BeautifulSoup
import pandas as pd
from dagster import asset, AssetExecutionContext


@asset(deps=["enterprises"], group_name="eu_enterprises", required_resource_keys={"mongo"})
def country_codes(context: AssetExecutionContext):
    url = 'https://en.wikipedia.org/wiki/ISO_3166-1'

    response = requests.get(url)
    parsed_data = BeautifulSoup(response.content, "html.parser")

    table = parsed_data.find_all('table')[2]
    full_name, two_letter_code, three_letter_code = ([], [], [])
    for row in table.find_all('tr'):
        if not row.find_all('th'):
            cells = row.find_all('td')
            full_name.append(cells[0].text.strip())
            two_letter_code.append(cells[1].text.strip())
            three_letter_code.append(cells[2].text.strip())

    df = pd.DataFrame({"full_name": full_name, "two_letter_code": two_letter_code, "three_letter_code": three_letter_code})
    country_codes_values = df.reset_index().to_dict("records")
    context.resources.mongo["country_codes"].insert_many(country_codes_values)