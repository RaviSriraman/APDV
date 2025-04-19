from dash import html, dcc
import plotly.express as px
import pandas as pd

from utils import mongo_utils, sql_db_utils
from utils.constants import PLOT_STYLE

work_timings = mongo_utils.find_all_working_times()
years = mongo_utils.find_all_years()


def year_employments_working_time_count():
    return html.Div(
        id="bar-year-employments-working-time-id",
        children=year_employments_working_time_count_component(), style=PLOT_STYLE)


def year_employments_working_time_count_component(work_timing=work_timings[0]):
    employments_df = mongo_utils.find_employments_by_working_time(work_timing)
    country_codes = mongo_utils.find_country_codes()
    country_codes = country_codes.rename(columns={"two_letter_code": "country_code"})
    employments_df = pd.merge(employments_df, country_codes, how="left", on="country_code")
    return [
        dcc.Dropdown(work_timings, work_timing, id='bar-year-employments-working-time-input', clearable=False),
        dcc.Graph(
            id='bar-year-employments-working-time-graph',
            figure=px.area(employments_df[["employees_in_thousands", "year", "country_code"]], x='year', y='employees_in_thousands',
                          title=f'Trend in Employee Count of {work_timing} Employees in Europe', color=employments_df["country_code"],
                           line_group="country_code")
        )

    ]

def line_year_employments_working_time_count():
    return html.Div(
        id="line-year-employments-working-time-id",
        children=line_year_employments_working_time_count_component(), style=PLOT_STYLE)


def line_year_employments_working_time_count_component(work_timing=work_timings[0]):
    employments_df = mongo_utils.find_employments_by_working_time(work_timing)
    country_codes = mongo_utils.find_country_codes()
    country_codes = country_codes.rename(columns={"two_letter_code": "country_code"})
    employments_df = pd.merge(employments_df, country_codes, how="left", on="country_code")
    return [
        dcc.Dropdown(work_timings, work_timing, id='line-year-employments-working-time-input', clearable=False),
        dcc.Graph(
            id='line-year-employments-working-time-graph',
            figure=px.line(employments_df[["employees_in_thousands", "year", "country_code"]], x='year', y='employees_in_thousands',
                          title=f'Trend in {work_timing} Employee Count in Europe', color=employments_df["country_code"],
                           line_group="country_code")
        )

    ]
