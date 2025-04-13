from dash import html, dcc
import plotly.express as px

from utils import mongo_utils
from utils.constants import PLOT_STYLE

cities = mongo_utils.find_all_enterprises()["city"].unique()

def city_wise_enterprise_count():
    return html.Div(
        id="city-enterprises-id",
        children=city_wise_enterprise_count_component(), style=PLOT_STYLE)


def city_wise_enterprise_count_component(city=cities[0]):
    enterprise_df = mongo_utils.find_enterprises_by_city(city)
    enterprises_by_city = enterprise_df.groupby(by=["year", "city"]).agg(
        {'enterprises': 'sum', "c_enterprises": "sum"}).reset_index()

    colors = enterprises_by_city['enterprises'].apply(lambda x: 'calculated' if x == 0 else 'provided')
    return [
        dcc.Dropdown(cities, city, id='city-selection'),
        dcc.Graph(
            id='city-enterprises-id-graph',
            figure=px.bar(enterprises_by_city[["c_enterprises", "year"]], x='year', y='c_enterprises',
                          title=f'Enterprises in {city}', color=colors)
        )
    ]
