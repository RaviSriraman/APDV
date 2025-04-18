from dash import Dash, callback

import dash_bootstrap_components as dbc

import utils.mongo_utils as mongo_utils
from pages.components.employments.country_employments_year_work_field import \
    country_employments_work_field_year_count_component
from pages.components.employments.year_employments_work_field import year_employments_work_field_count_component
from pages.components.employments.year_employments_working_time import year_employments_working_time_count_component, line_year_employments_working_time_count_component
from pages.components.enterprises.city_wise_enterprise import city_wise_enterprise_count_component
from pages.components.enterprises.year_wise_enterprise import enterprises_by_year_country_map_component
from pages.components.enterprises.country_wise_enterprise import country_wise_enterprise_count_component, \
    country_wise_pie_chart_component, country_enterprises_year_bar_chart_component
from pages.components.tourism.country_spent_year import tourism_country_spent_year_bar_component
from pages.components.tourism.tourism_expenditures import tourism_expenditure_country_spent_year_line_component
from pages.components.tourism.year_spent_country import tourism_year_spent_line_component
from pages.main import main_page
from pages.components.combined.combined_components import country_spent_enterprises_year_line_component, country_spent_enterprises_year_bar_component
from dotenv import load_dotenv

from utils.constants import (COUNTRY_ENTERPRISE_YEAR_MAP_IO,
                             COUNTRY_ENTERPRISES_YEAR_BAR_IO,
                             COUNTRY_ENTERPRISES_YEAR_PIE_IO,
                             YEAR_ENTERPRISE_CITY_BAR_IO,
                             YEAR_ENTERPRISES_COUNTRY_LOCATION_BAR_IO,
                             ENTERPRISES_TOURISM_SPENTS_LINE_IO,
                             ENTERPRISES_TOURISM_SPENTS_BAR_IO,
                             EMPLOYMENTS_YEAR_WORK_FIELD_BAR_IO,
                             EMPLOYMENTS_YEAR_WORKING_TIME_LINE_IO,
                             EMPLOYMENTS_COUNTRY_WORKIN_FIELD_AREA_IO,
                             EMPLOYMENTS_YEAR_WORKING_TIME_BAR_IO,
                             TOURISM_COUNTRY_SPENT_YEAR_LINE_IO,
                             TOURISM_COUNTRY_SPENT_YEAR_BAR_IO,
                             TOURISM_EXPENDITURE_YEAR_SPENT_COUNTRY_LINE_IO)

cities = mongo_utils.find_all_enterprises()["city"].unique()
countries = mongo_utils.find_all_enterprises()["country"].unique()
indic_urs = mongo_utils.find_all_enterprises()["indic_ur"].unique()


@callback(*COUNTRY_ENTERPRISES_YEAR_BAR_IO)
def update_year_wise_enterprise_count(year):
    return country_enterprises_year_bar_chart_component(year)


@callback(*YEAR_ENTERPRISE_CITY_BAR_IO)
def update_city_wise_enterprise_count(city_value):
    return city_wise_enterprise_count_component(city_value)


@callback(*YEAR_ENTERPRISES_COUNTRY_LOCATION_BAR_IO)
def update_country_wise_enterprise_count(country_value, indic_ur):
    return country_wise_enterprise_count_component(country_value, indic_ur)


@callback(*COUNTRY_ENTERPRISES_YEAR_PIE_IO)
def update_city_wise_enterprise_count(year):
    return country_wise_pie_chart_component(year)


@callback(*COUNTRY_ENTERPRISE_YEAR_MAP_IO)
def update_europe_country_wise_enterprise_count(year):
    return enterprises_by_year_country_map_component(year)


@callback(*ENTERPRISES_TOURISM_SPENTS_LINE_IO)
def update_europe_year_enterprises_tourism_spends_country_line_chart(country):
    return country_spent_enterprises_year_line_component(country)

@callback(*ENTERPRISES_TOURISM_SPENTS_BAR_IO)
def update_europe_year_enterprises_tourism_spends_country_bar_chart(year):
    return country_spent_enterprises_year_bar_component(year)

@callback(*EMPLOYMENTS_YEAR_WORK_FIELD_BAR_IO)
def update_employments_year_work_field_bar_chart(work_field):
    return year_employments_work_field_count_component(work_field)

@callback(*EMPLOYMENTS_YEAR_WORKING_TIME_BAR_IO)
def update_employments_year_working_time_bar_chart(working_time):
    return year_employments_working_time_count_component(working_time)

@callback(*EMPLOYMENTS_YEAR_WORKING_TIME_LINE_IO)
def update_employments_year_working_time_line_chart(working_time):
    return line_year_employments_working_time_count_component(working_time)

@callback(*EMPLOYMENTS_COUNTRY_WORKIN_FIELD_AREA_IO)
def update_employments_country_working_field_area_chart(work_field):
    return country_employments_work_field_year_count_component(work_field)

@callback(*TOURISM_COUNTRY_SPENT_YEAR_LINE_IO)
def update_tourism_year_spent_country_line_chart(purpose):
    return tourism_year_spent_line_component(purpose)

@callback(*TOURISM_COUNTRY_SPENT_YEAR_BAR_IO)
def update_tourism_country_spent_year_bar_chart(year):
    return tourism_country_spent_year_bar_component(year)


@callback(*TOURISM_EXPENDITURE_YEAR_SPENT_COUNTRY_LINE_IO)
def update_tourism_expenditure_country_spent_year_line_chart(year):
    return tourism_expenditure_country_spent_year_line_component(year)



if __name__ == '__main__':
    load_dotenv()
    app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    app.layout = main_page()
    app.run(debug=True, port=8070, host="0.0.0.0")
