from dash import html
import dash_bootstrap_components as dbc

from .components.combined.combined_components import country_spent_enterprises_year_line, country_spent_enterprises_year_bar


def combined_dashboard():
    return (
        dbc.Tab(
            dbc.Card(
                [
                    dbc.CardBody(
                        [
                            html.Div(children=[
                                html.H3(children='Tourism vs Enterprises',
                                        style={"background": "blue", "color": "white", "padding": "15px",
                                               "border-style": "solid", "border-color": "gold"}),
                                country_spent_enterprises_year_line(),
                                country_spent_enterprises_year_bar()
                            ])
                        ]
                    )
                ]
            ),
            label="Combined Results",
            activeLabelClassName="bg-light",
        ))
