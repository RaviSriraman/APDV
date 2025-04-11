import pandas as pd
from dash import html, dcc
import plotly.express as px

from components.country_wise_enterprise import country_wise_enterprise_count, country_wise_pie_chart
from components.city_wise_enterprise import city_wise_enterprise_count
from components.year_wise_enterprise import year_wise_enterprise_count
from utils import mongo_utils
from utils.constants import PLOT_STYLE


def map_plot():
    all_enterprises: pd.DataFrame = mongo_utils.find_all_enterprises()
    enterprises_2012 = (all_enterprises[all_enterprises["year"] == 2012].groupby(by=["country"])
     .agg({'enterprises': 'sum'}).sort_values(by="enterprises").reset_index())
    country_codes: pd.DataFrame = mongo_utils.find_country_codes().rename(columns={"two_letter_code": "country"})

    new_df = pd.merge(enterprises_2012, country_codes, on=["country"])
    return html.Div(
        id='map-year-wise-enterprise-count-id',
        children=[
            dcc.Dropdown(all_enterprises["year"].unique(), 2012, id='map-year-selection-id'),
            dcc.Graph(
                id='map-enterprises-by-year-graph',
                figure=px.choropleth(new_df, locations="three_letter_code",
                        color="enterprises",
                        hover_name="country",
                        scope="europe",
                        color_continuous_scale=px.colors.sequential.Plasma)
            )
        ], style=PLOT_STYLE)


def dashboard():

    return html.Div(children=[
        html.H1(children='European Enterprises'),
        year_wise_enterprise_count(),
        city_wise_enterprise_count(),
        country_wise_enterprise_count(),
        country_wise_pie_chart(),
        map_plot()
    ])