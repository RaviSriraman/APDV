from dash import html, dcc
import plotly.express as px
from utils import mongo_utils

from utils.constants import PLOT_STYLE

countries = mongo_utils.find_all_enterprises()["country"].unique()

def country_wise_enterprise_count():
    all_enterprises = mongo_utils.find_enterprises_by_county('FR').groupby(by=["year", "country"]).agg(
        {'enterprises': 'sum'}).reset_index()
    return html.Div(
        id="country-enterprises-id",
        children=[
            dcc.Dropdown(countries, 'FR', id='country-selection-id'),
            dcc.Graph(
                id='country-enterprises-id-graph',
                figure=px.bar(all_enterprises[["enterprises", "year"]], x='year', y='enterprises',
                              title='Enterprises in top countries')
            )
        ], style=PLOT_STYLE)

def country_wise_pie_chart():
    year = mongo_utils.find_all_enterprises()["year"].unique()
    all_enterprises = mongo_utils.find_enterprises_by_year(2012).groupby(by=["year", "country"]).agg(
        {'enterprises': 'sum'}).reset_index()
    return html.Div(
        id="pie-country-enterprises-id",
        children=[
            dcc.Dropdown(year, 2012, id='pie-country-selection-id'),
            dcc.Graph(
                id='pie-country-enterprises-id-graph',
                figure=px.pie(all_enterprises[["enterprises", "country"]].sort_values(by="enterprises", ascending=False).head(5), values='enterprises', names='country',
                              title='Enterprises in top countries')
            )
        ], style=PLOT_STYLE)
