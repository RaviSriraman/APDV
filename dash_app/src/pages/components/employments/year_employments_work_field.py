from dash import html, dcc
import plotly.express as px

from utils import mongo_utils
from utils.constants import PLOT_STYLE

work_fields = mongo_utils.find_all_work_fields()

def year_employments_work_field_count():
    return html.Div(
        id="bar-year-employments-work-field-id",
        children=year_employments_work_field_count_component(), style=PLOT_STYLE)


def year_employments_work_field_count_component(work_field=work_fields[0]):
    employments_df = mongo_utils.find_employments_by_work_field(work_field)
                      # .groupby(by=["year", "work_field"]).agg({"employees_in_thousands": "sum"}).reset_index()
    return [
        dcc.Dropdown(work_fields, work_field, id='bar-year-employments-work-field-input', clearable=False),
        dcc.Graph(
            id='bar-year-employments-work-field-graph',
            figure=px.bar(employments_df[["employees_in_thousands", "year"]], x='year', y='employees_in_thousands',
                          title=f'Trend in Employment in {work_field} Sector in Europe', color=employments_df["country_code"])
        )
    ]