from dash import html, dcc
import plotly.express as px
from utils import mongo_utils

from utils.constants import PLOT_STYLE


def country_wise_enterprise_count():
    all_enterprises = mongo_utils.find_all_enterprises()
    return html.Div(
        id="country-enterprises-id",
        children=[
            dcc.Dropdown(all_enterprises["country"].unique(), 'FR', id='country-selection-id'),
            dcc.Graph(
                id='country-enterprises-id-graph',
                figure=px.bar(all_enterprises[["enterprises", "year"]], x='year', y='enterprises',
                              title='Enterprises in top cities')
            )
        ], style=PLOT_STYLE)
