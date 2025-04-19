from dash import html, dcc
import plotly.express as px
import pandas as pd

from utils import mongo_utils, sql_db_utils
from utils.constants import PLOT_STYLE

cities = mongo_utils.find_all_enterprises_by_city()["city"].unique()
city_codes = sql_db_utils.find_city_codes()
city_full_names = list(city_codes[city_codes["city"].isin(cities)]["city_name"])

def city_wise_enterprise_count():
    return html.Div(
        id="city-enterprises-id",
        children=city_wise_enterprise_count_component(), style=PLOT_STYLE)


def city_wise_enterprise_count_component(city_name=city_full_names[0]):
    city = city_codes[city_codes["city_name"] == city_name]["city"].iloc[0]
    enterprise_df = mongo_utils.find_enterprises_by_city(city)
    if enterprise_df.empty:
        return [
            dcc.Dropdown(city_full_names, city_name, id='city-selection', clearable=False,),
            dcc.Graph(
                id='city-enterprises-id-graph',
                figure=px.box(pd.DataFrame({"year": [], "c_enterprises": []}), x='year', y='c_enterprises',
                              title=f'No data present.Please select some other options."')
            )

        ]
    enterprises_by_city = enterprise_df.groupby(by=["year", "city"]).agg(
        {'enterprises': 'sum', "c_enterprises": "sum"}).reset_index()

    enterprises_by_city = pd.merge(enterprises_by_city, city_codes, how="left", on="city")
    colors = enterprises_by_city['enterprises'].apply(lambda x: 'Projected' if x == 0 else 'Given')
    return [
        dcc.Dropdown(city_full_names, city_name, id='city-selection'),
        dcc.Graph(
            id='city-enterprises-id-graph',
            figure=px.bar(enterprises_by_city[["c_enterprises", "year"]], x='year', y='c_enterprises',
                          title=f'Trend in Number of Companies in {city_name}', color=colors)
        )
    ]
