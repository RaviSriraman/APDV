from dash import html, dcc
import plotly.express as px

from utils import mongo_utils
from utils.constants import PLOT_STYLE

all_enterprises = mongo_utils.find_all_enterprises()


def year_wise_enterprise_count():
    all_enterprises = mongo_utils.find_all_enterprises()
    enterprises_2012 = (all_enterprises[all_enterprises["year"] == 2012].groupby(by=["country", "year"])
                        .agg({'enterprises': 'sum'})
                        .sort_values(by="enterprises").reset_index())
    enterprises_2012 = enterprises_2012[enterprises_2012["enterprises"] > 0]
    return html.Div(
        id='year-wise-enterprise-count-id',
        children=[
        dcc.Dropdown(all_enterprises["year"].unique(), 2012, id='year-selection-id'),
        dcc.Graph(
            id='enterprises-by-year-graph',
            figure=px.bar(enterprises_2012, y='enterprises', x='country',
                          title=f'Enterprises in top countries in year 2012')
        )
    ], style=PLOT_STYLE)