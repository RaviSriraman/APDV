from dash import html
import dash_bootstrap_components as dbc
from .components.tourism.country_spent_year import tourism_country_spent_year_bar
from .components.tourism.tourism_expenditures import tourism_expenditure_country_spent_year_line
from .components.tourism.year_spent_country import tourism_year_spent_country_line


def tourism_dashboard():
    return (
        dbc.Tab(
            dbc.Card(
                [
                    dbc.CardBody(
                        [
                            html.Div(children=[
                                html.H3(children='Tourism in Europe',
                                        style={"background": "blue", "color": "white", "padding": "15px",
                                               "border-style": "solid", "border-color": "gold"}),
                                tourism_country_spent_year_bar(),
                                tourism_year_spent_country_line(),
                                tourism_expenditure_country_spent_year_line()
                            ])

                        ]
                    )
                ]
            ),
            label="Tourism",
            activeLabelClassName="bg-light",
        ))
