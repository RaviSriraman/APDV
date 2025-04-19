from dash import html, dcc
import plotly.express as px

from utils.constants import PLOT_STYLE
from utils.mongo_utils import  fetch_tours_by_purpose_destination_year, fetch_all_tour_years

years = fetch_all_tour_years()

def tourism_country_spent_year_bar_component(year=int(years[0])):
    tours_df = fetch_tours_by_purpose_destination_year(year)

    return [
        dcc.Dropdown(years, year, id='tourism-bar-country-amount-year-input', clearable=False),
        dcc.Graph(
            id='tourism-bar-country-amount-year-graph',
            figure=px.bar(tours_df, x="c_dest", y="amount", color="Purpose", title=f"Distribution of Tourism Expenditures in {year}")
        )
    ]


def tourism_country_spent_year_bar():
    return html.Div(
        id="tourism-bar-country-amount-year-id",
        children=tourism_country_spent_year_bar_component(), style=PLOT_STYLE)
