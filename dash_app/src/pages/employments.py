from dash import html
import dash_bootstrap_components as dbc
from .components.employments.year_employments_work_field import year_employments_work_field_count
from .components.employments.year_employments_working_time import (year_employments_working_time_count,
                                                                   line_year_employments_working_time_count)
from .components.employments.country_employments_year_work_field import country_employments_work_field_year_count

def employments_dashboard():
    return (
        dbc.Tab(
            dbc.Card(
                [
                    dbc.CardBody(
                        [
                            html.Div(children=[
                                html.H3(children='Employments in Tourism',
                                        style={"background": "blue", "color": "white", "padding": "15px",
                                               "border-style": "solid", "border-color": "gold"}),
                                year_employments_work_field_count(),
                                year_employments_working_time_count(),
                                line_year_employments_working_time_count(),
                                country_employments_work_field_year_count()
                            ])

                        ]
                    )
                ]
            ),
            label="Employments in Tourism",
            activeLabelClassName="bg-light",
        ))