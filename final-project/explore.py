import pandas as pd
from io import StringIO
import json


def add_country(entry, county, valuation_date):
    entry['County'] = county
    entry['ValuationDate'] = valuation_date
    return entry

if __name__ == '__main__':
    # df = pd.DataFrame({'a': ["abcd"]})
    # df["b"] = df["a"][:2]
    # print(df.head())
    result = []
    v_df = pd.read_csv("./valuation.csv")
    print(v_df.columns)
    for e in v_df.groupby(by=["County", "ValuationDate"]):
        # print(pd.DataFrame(e[1]["ValuationReport"]).columns)
        for e2 in e[1]["ValuationReport"]:
            row = map(lambda x: add_country(x, e[0][0], e[0][1]), json.loads(e2.replace("'", "\"")))
            result += row

    report_df = pd.DataFrame(result)
    mean_value = report_df.groupby(by=["County", "FloorUse", "ValuationDate"])["NavPerM2"].mean(numeric_only=True)
    report_df = report_df.set_index(['County', 'FloorUse', "ValuationDate"])
    report_df['MeanNavPerM2'] = mean_value.round()
    report_df = report_df.reset_index()
    final_result = report_df.sort_values(ascending=False, by=["County", 'FloorUse', "ValuationDate"])

    print(final_result.head())