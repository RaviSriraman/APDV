from dash import html, dcc
import plotly.express as px

from utils import mongo_utils
from utils.constants import PLOT_STYLE

all_enterprises = mongo_utils.find_all_enterprises()

def city_wise_enterprise_count():
    return html.Div(
        id="city-enterprises-id",
        children=[
            dcc.Dropdown(all_enterprises["city"].unique(), 'FR', id='city-selection'),
            dcc.Graph(
                id='city-enterprises-id-graph',
                figure=px.bar(all_enterprises[["enterprises", "year"]], x='year', y='enterprises',
                              title='Enterprises in top cities')
            )
        ], style=PLOT_STYLE)