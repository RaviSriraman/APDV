from dash import html, dcc
import plotly.express as px
import pandas as pd

from utils import mongo_utils
from utils.constants import PLOT_STYLE

years = mongo_utils.find_all_years()

def enterprises_by_year_country():
    return html.Div(
        id='map-year-wise-enterprise-count-id',
        children=enterprises_by_year_country_map_component(), style=PLOT_STYLE)


def year_enterprise_country_line():
    return html.Div(
        id='line-year-enterprise-country-id',
        children=year_enterprise_country_line_component(), style=PLOT_STYLE)


def year_enterprise_country_line_component():
    enterprises_df = mongo_utils.find_all_enterprises_group_by_country()
    enterprises_df = enterprises_df[((enterprises_df["enterprises"] != 0) & enterprises_df["country"].isin(["UK", "FR", "IT",  "NL", "CZ"]))]
    enterprises_df = enterprises_df.groupby(by=["country", "year"]).agg({"c_enterprises": "sum"}).reset_index()
    return [
        dcc.Graph(
            id='line-enterprises-year-country-graph',
            figure=px.line(enterprises_df, x="year",
                                 y="c_enterprises",
                                 color="country")
        )
    ]

def enterprises_by_year_country_map_component(year=years[0]):

    enterprises = mongo_utils.find_all_by_country_year(year).sort_values(by="c_enterprises")
    enterprises = enterprises[enterprises["c_enterprises"] != 0]
    country_codes: pd.DataFrame = mongo_utils.find_country_codes().rename(columns={"two_letter_code": "country"})
    new_df = pd.merge(enterprises, country_codes, on=["country"])
    return [
        dcc.Dropdown(years, year, id='map-year-selection-id'),
        dcc.Graph(
            id='map-enterprises-by-year-graph',
            figure=px.choropleth(new_df, locations="three_letter_code",
                                 color="c_enterprises",
                                 hover_name="full_name",
                                 scope="europe",
                                 color_continuous_scale=px.colors.sequential.Plasma)
        )
    ]
