from dash import html
import dash_bootstrap_components as dbc

from .components.enterprises.country_wise_enterprise import (country_wise_enterprise_count,
                                                             country_wise_pie_chart,
                                                             year_wise_enterprise_count)
from .components.enterprises.city_wise_enterprise import city_wise_enterprise_count
from .components.enterprises.year_wise_enterprise import enterprises_by_year_country, year_enterprise_country_line


def enterprise_dashboard():
    return (
        dbc.Tab(
            dbc.Card(
                [
                    dbc.CardBody(
                        [
                            html.Div(children=[
                                html.H3(children='Companies in Europe',
                                        style={"background": "blue", "color": "white", "padding": "15px",
                                               "border-style": "solid", "border-color": "gold"}),
                                year_wise_enterprise_count(),
                                city_wise_enterprise_count(),
                                country_wise_enterprise_count(),
                                country_wise_pie_chart(),
                                enterprises_by_year_country(),
                                year_enterprise_country_line()
                            ])
                        ]
                    )
                ]
            ),
            label="Companies",
            activeLabelClassName="bg-light",
        ))
