from dash import html, dcc
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

from models.tours import fetch_domestic_tours_by_country_all_purpose_enterprises, \
    fetch_domestic_tours_by_country_all_purpose_enterprises_by_country
from utils import mongo_utils, sql_db_utils
from utils.constants import PLOT_STYLE
from utils.common_utils import get_first_or_empty

enterprises = mongo_utils.find_all_enterprises()
country_codes = mongo_utils.find_country_codes()
years = sql_db_utils.find_all_years()
destinations = sql_db_utils.find_all_destinations()
purposes = sql_db_utils.find_all_purposes()


def plotly_dual_axis(data1, data2, x="", title="", y1="", y2=""):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=data1[x], y=data1[y1], name='Companies'), secondary_y=False)
    fig.add_trace(go.Scatter(x=data2[x], y=data2[y2], name='Tourism Expenditures'), secondary_y=True)
    fig.update_layout(title=title, yaxis=dict(title=y1), yaxis2=dict(title=y2), xaxis=dict(title=x))
    return fig


def plotly_dual_axis_bar(data1, data2, x="", title="", y1="", y2=""):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=data1[x], y=data1[y1], name='Companies', offsetgroup=1), secondary_y=False)
    fig.add_trace(go.Bar(x=data2[x], y=data2[y2], name='Tourism Expenditures', offsetgroup=2), secondary_y=True)
    fig.update_layout(title=title, yaxis=dict(title=y1), yaxis2=dict(title=y2), xaxis=dict(title=x))
    return fig


def country_spent_enterprises_year_line_component(country='Italy'):
    tours_enterprises = fetch_domestic_tours_by_country_all_purpose_enterprises_by_country(country)
    countries = list(enterprises["country"].unique())
    country_names = list(country_codes[country_codes["two_letter_code"].isin(countries)]["full_name"])
    if tours_enterprises.empty:
        return [
            dcc.Dropdown(country_names, country, id='line-combined-country-spent-year-input'),
            dcc.Graph(
                id='line-combined-country-spent-year-graph',
                figure=px.box(pd.DataFrame({"x": [], "y": []}), x='x', y='y',
                              title=f'No data present.Please select some other options."')
            )
        ]

    tours_enterprises = tours_enterprises[
        (tours_enterprises["country_name"] == country) & (tours_enterprises["indic_ur"] == "EC2021V")]
    return [
        dcc.Dropdown(country_names, country, id='line-combined-country-spent-year-input', clearable=False),
        dcc.Graph(
            id='line-combined-country-spent-year-graph',
            figure=plotly_dual_axis(tours_enterprises[["year", "c_enterprises"]], tours_enterprises[["year", "amount"]],
                                    "year", f"Trend in Number of Companies and Money Spent on Tourism", "c_enterprises", "amount")
        )
    ]


def country_spent_enterprises_year_line():
    return html.Div(
        id="line-combined-country-spent-enterprises_year-id",
        children=country_spent_enterprises_year_line_component(), style=PLOT_STYLE)

