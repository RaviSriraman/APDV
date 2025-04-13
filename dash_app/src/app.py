from dash import Dash, dcc, callback, html

import dash_bootstrap_components as dbc
import plotly.express as px

import utils.mongo_utils as mongo_utils
import utils.sql_db_utils  as sql_utils
from components.city_wise_enterprise import city_wise_enterprise_count_component
from components.year_wise_enterprise import enterprises_by_year_country_map_component
from components.country_wise_enterprise import country_wise_enterprise_count_component, country_wise_pie_chart_component, country_enterprises_year_bar_chart_component
from pages.main import enterprise_dashboard
from dotenv import load_dotenv

from utils.constants import (COUNTRY_ENTERPRISE_YEAR_MAP_IO, COUNTRY_ENTERPRISES_YEAR_BAR_IO,
                             COUNTRY_ENTERPRISES_YEAR_PIE_IO, YEAR_ENTERPRISE_CITY_BAR_IO, YEAR_ENTERPRISES_COUNTRY_LOCATION_BAR_IO)

cities = mongo_utils.find_all_enterprises()["city"].unique()
countries = mongo_utils.find_all_enterprises()["country"].unique()
indic_urs = mongo_utils.find_all_enterprises()["indic_ur"].unique()

@callback(*COUNTRY_ENTERPRISES_YEAR_BAR_IO)
def update_year_wise_enterprise_count(year):
    return country_enterprises_year_bar_chart_component(year)


@callback(*YEAR_ENTERPRISE_CITY_BAR_IO)
def update_city_wise_enterprise_count(city_value):
    return city_wise_enterprise_count_component(city_value)


@callback(*YEAR_ENTERPRISES_COUNTRY_LOCATION_BAR_IO)
def update_country_wise_enterprise_count(country_value, indic_ur):
    return country_wise_enterprise_count_component(country_value, indic_ur)


@callback(*COUNTRY_ENTERPRISES_YEAR_PIE_IO)
def update_city_wise_enterprise_count(year):
    return country_wise_pie_chart_component(year)

@callback(*COUNTRY_ENTERPRISE_YEAR_MAP_IO)
def update_europe_country_wise_enterprise_count(year):
    return enterprises_by_year_country_map_component(year)


# Run the app
if __name__ == '__main__':
    load_dotenv()
    title = dcc.Markdown("Impact of Tourism on Enterprises", className="bg-light", style={"font-size": 30})
    app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    list_of_tabs = [
        dbc.Tab(
            dbc.Card(
                [
                    dbc.CardBody(
                        [
                            enterprise_dashboard()
                        ]
                    )
                ]
            ),
            label="Enterprises",
            activeLabelClassName="bg-light",
        ),
        dbc.Tab(
            dbc.Card(
                [
                    dbc.CardBody(
                        [
                            html.Div(sql_utils.fetch_by_year(2012).__str__())

                        ]
                    )
                ]
            ),
            label="Tourism",
            activeLabelClassName="bg-light",
        ),
        dbc.Tab(
            dbc.Card(
                [
                    dbc.CardBody(
                        [
                            html.Div("")
                        ]
                    )
                ]
            ),
            label="Enterprises Tourism",
            activeLabelClassName="bg-light",
        )
    ]

    app.layout = dbc.Container(
        [
            dbc.Row([
                dbc.Col([title], width=12, style={"text-align": "center", "margin": "auto"})
            ]),

            dbc.Tabs(list_of_tabs)
        ]
    )
    app.run(debug=True, port=8070, host="0.0.0.0")
