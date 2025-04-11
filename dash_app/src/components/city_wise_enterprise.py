from dash import html, dcc
import plotly.express as px

from utils import mongo_utils
from utils.constants import PLOT_STYLE

cities = mongo_utils.find_all_enterprises()["city"].unique()

def city_wise_enterprise_count():
    all_enterprises = mongo_utils.find_enterprises_by_city('FR').groupby(by=["year", "city"]).agg(
        {'enterprises': 'sum'}).reset_index()

    return html.Div(
        id="city-enterprises-id",
        children=[
            dcc.Dropdown(cities, 'FR', id='city-selection'),
            dcc.Graph(
                id='city-enterprises-id-graph',
                figure=px.bar(all_enterprises[["enterprises", "year"]], x='year', y='enterprises',
                              title='Enterprises in top cities')
            )
        ], style=PLOT_STYLE)