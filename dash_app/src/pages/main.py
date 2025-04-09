from dash import html, dcc
import plotly.express as px

from components.country_wise_enterprise import country_wise_enterprise_count
from components.city_wise_enterprise import city_wise_enterprise_count
from components.year_wise_enterprise import year_wise_enterprise_count
from utils import mongo_utils
from utils.constants import PLOT_STYLE

pie_chart = html.Div([dcc.Graph(id="graph"), html.P("Names:"),
                    dcc.Dropdown(id="names", options=["smoker", "day", "time", "sex"], value="day", clearable=False, ),
                    html.P("Values:"),
                    dcc.Dropdown(id="values", options=["total_bill", "tip", "size"], value="total_bill",
                                 clearable=False, ), ])

def dashboard():
    return html.Div(children=[
        html.H1(children='European Tourism and Enterprises'),
        year_wise_enterprise_count(),
        city_wise_enterprise_count(),
        country_wise_enterprise_count(),
        # pie_chart
    ])