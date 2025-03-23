import requests
import pandas as pd

def fetch_local_authorities():
    return requests.get("https://opendata.tailte.ie/api/Property/SearchLocalAuthority").json()

if __name__ == '__main__':
    result = []
    for local_authority in fetch_local_authorities():
        print(local_authority)
        url = f"https://opendata.tailte.ie/api/Property/GetProperties?Fields=*&Format=json&Download=false&LocalAuthority={local_authority['LaDesc']}"
        response = requests.get(url).json()
        result += response

    print(len(result))
    df = pd.DataFrame(result)
    df.to_csv("./valuation.csv")


