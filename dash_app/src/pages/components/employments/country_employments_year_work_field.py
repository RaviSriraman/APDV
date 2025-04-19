from dash import html, dcc
import plotly.express as px

from utils import mongo_utils
from utils.constants import PLOT_STYLE

years = list(map(lambda x: int(x), mongo_utils.find_all_years_from_employments()))

def country_employments_work_field_year_count():
    return html.Div(
        id="area-country-employments-work-field-year-id",
        children=country_employments_work_field_year_count_component(), style=PLOT_STYLE)


def country_employments_work_field_year_count_component(year=years[0]):
    employments_df = mongo_utils.find_employments_by_year(year)
    work_fields = {
        "Air transport": "Air",
        "Accommodation and food service activities": "Acc & Food",
        "Travel agency, tour operator and other reservation service and related activities": "Travel",
        "Total - all NACE activities": "Total",
        "Accommodation": "acc"
    }
    employments_df = employments_df[employments_df["work_field"] != "Total - all NACE activities"]
    colors = employments_df["work_field"].apply(lambda x: work_fields[x])

    return [
        dcc.Dropdown(years, year, id='area-year-employments-work-field-year-input'),
        dcc.Graph(
            id='area-country-employments-work-field-year-graph',
            figure=px.bar(employments_df[["employees_in_thousands", "country_name", "work_field"]], x='country_name',
                           y='employees_in_thousands',
                          title=f'Distribution in Employment in Different Sector in {year}', color=colors)
        )
    ]