from dash import html

from components.country_wise_enterprise import (country_wise_enterprise_count,
                                                country_wise_pie_chart, year_wise_enterprise_count)
from components.city_wise_enterprise import city_wise_enterprise_count
from components.year_wise_enterprise import enterprises_by_year_country, year_enterprise_country_line
from utils import mongo_utils
from utils.constants import PLOT_STYLE


def enterprise_dashboard():

    return html.Div(children=[
        html.H1(children='European Enterprises'),
        year_wise_enterprise_count(),
        city_wise_enterprise_count(),
        country_wise_enterprise_count(),
        country_wise_pie_chart(),
        enterprises_by_year_country(),
        year_enterprise_country_line()
    ])