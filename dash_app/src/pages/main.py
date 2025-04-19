import dash_bootstrap_components as dbc
from dash import dcc, html

from .combined import combined_dashboard
from .enterprises import enterprise_dashboard
from .tourism import tourism_dashboard
from .employments import employments_dashboard

title = dcc.Markdown(children="Companies, Employment, and Tourism in Europe", className="bg-light", style={"font-size": 30})

def main_page():
    return dbc.Container(
        [
            dbc.Row([
                dbc.Col([title], width=12, style={"text-align": "center", "margin": "auto"})
            ]),
            dbc.Tabs(
                children=[enterprise_dashboard(), employments_dashboard(), tourism_dashboard(), combined_dashboard()])

        ]
    )