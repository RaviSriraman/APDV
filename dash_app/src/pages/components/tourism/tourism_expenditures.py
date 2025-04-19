from dash import html, dcc
import plotly.express as px
from utils.constants import PLOT_STYLE
from utils.sql_db_utils import  find_all_expenditures, fetch_tours_data_by_expenditure_destination_country

expenditures = find_all_expenditures()

def tourism_expenditure_country_spent_year_line_component(expenditure=expenditures[0]):
    tours_df = fetch_tours_data_by_expenditure_destination_country(expenditure)
    return [
        dcc.Dropdown(expenditures, expenditure, id='tourism-expenditure-country-spent-year-line-input', clearable=False),
        dcc.Graph(
            id='tourism-expenditure-country-spent-year-line-graph',
            figure=px.line(tours_df, x="year", y="amount", color="country", title=f"Trend in {expenditure}")
        )
    ]


def tourism_expenditure_country_spent_year_line():
    return html.Div(
        id="tourism-expenditure-country-spent-year-line-id",
        children=tourism_expenditure_country_spent_year_line_component(), style=PLOT_STYLE)

