from io import StringIO
from urllib.request import urlopen
import pandas as pd


def replace_content(file_path: str):
    response = urlopen("https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/urb_cecfi?format=TSV")
    with open("./new_file.tsv", "wb") as file:
        file.write(response.read())

    with open("./new_file.tsv", "r") as file:
        content = file.read()
        content = content.replace("\t", ",").replace(",:", ",0")
        return pd.read_csv(StringIO(content), delimiter=",")


if __name__ == '__main__':
    df = replace_content("")
    print(df.columns)
