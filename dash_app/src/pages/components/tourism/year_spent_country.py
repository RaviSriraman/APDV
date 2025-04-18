from dash import html, dcc
import plotly.express as px
from utils.constants import PLOT_STYLE
from utils.mongo_utils import  fetch_tours_by_purpose_destination_country, fetch_all_tour_purposes

purposes = fetch_all_tour_purposes()

def tourism_year_spent_line_component(purpose=purposes[0]):
    tours_df = fetch_tours_by_purpose_destination_country(purpose)

    return [
        dcc.Dropdown(purposes, purpose, id='tourism-line-year-amount-purpose-input', clearable=False),
        dcc.Graph(
            id='tourism-line-year-amount-purpose-graph',
            figure=px.line(tours_df, x="year", y="amount", color="destination_country", title=f"Trend in Expenditure in {purpose} Tourism")
        )
    ]


def tourism_year_spent_country_line():
    return html.Div(
        id="tourism-line-year-amount-purpose-id",
        children=tourism_year_spent_line_component(), style=PLOT_STYLE)
