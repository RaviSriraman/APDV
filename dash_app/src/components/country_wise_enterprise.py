from dash import html, dcc
import plotly.express as px
import pandas as pd
from utils import mongo_utils

from utils.constants import PLOT_STYLE

from dash_app.src.utils.constants import LOCATIONS, INDIC_URS, REV_INDIC_URS

enterprises = mongo_utils.find_all_enterprises()
countries = enterprises["country"].unique()
indic_urs = enterprises["indic_ur"].unique()
years = mongo_utils.find_all_years()


def country_wise_enterprise_count():
    return html.Div(
        id="country-enterprises-id",
        children=country_wise_enterprise_count_component(countries[0], INDIC_URS[indic_urs[0]]),
        style=PLOT_STYLE)


def country_wise_pie_chart():
    return html.Div(
        id="pie-country-enterprises-id",
        children=country_wise_pie_chart_component(years[0]),
        style=PLOT_STYLE)


def year_wise_enterprise_count():
    return html.Div(
        id='year-wise-enterprise-count-id',
        children=country_enterprises_year_bar_chart_component(years[0]),
        style=PLOT_STYLE)


def country_wise_pie_chart_component(year):
    df = mongo_utils.find_enterprises_by_year_group_by_country(year)
    return [
        dcc.Dropdown(years, year, id='pie-country-selection-id'),
        dcc.Graph(
            id='pie-country-enterprises-id-graph',
            figure=px.pie(
                df[["c_enterprises", "country"]].sort_values(by="c_enterprises", ascending=False).head(5),
                values='c_enterprises', names='country',
                title='Enterprises in top countries')
        )
    ]


def country_wise_enterprise_count_component(country_value, indic_ur):
    enterprise_df = mongo_utils.find_enterprises_by_country_and_indic_ur(country_value, REV_INDIC_URS[indic_ur])
    if enterprise_df.empty:
        return [
            dcc.Dropdown(countries, country_value,
                         id='country-selection-id'),
            dcc.Dropdown(LOCATIONS, indic_ur, id='indic-selection-id'),
            dcc.Graph(
                id='country-enterprises-id-graph',
                figure=px.box(pd.DataFrame({"year": [], "c_enterprises": []}), x='year', y='c_enterprises',
                              title=f'No data present.Please select some other options."')
            )

        ]
    colors = enterprise_df['enterprises'].apply(lambda x: 'calculated' if x == 0 else 'provided')
    return [
        dcc.Dropdown(countries, country_value, id='country-selection-id'),
        dcc.Dropdown(LOCATIONS, indic_ur, id='indic-selection-id'),
        dcc.Graph(
            id='country-enterprises-id-graph',
            figure=px.bar(enterprise_df[["c_enterprises", "year"]], x='year', y='c_enterprises',
                          title=f'Enterprises in {country_value}', color=colors)
        )
    ]


def country_enterprises_year_bar_chart_component(year):
    enterprises_df = mongo_utils.find_all_by_country_year(year).sort_values(by="c_enterprises").tail(10)[::-1]
    return [
        dcc.Dropdown(years, year, id='year-selection-id'),
        dcc.Graph(
            id='enterprises-by-year-graph',
            figure=px.bar(enterprises_df, y='c_enterprises', x='country',
                          title=f'Enterprises in top countries in year {year}')
        )
    ]
