from dash import html, dcc
import plotly.express as px
import pandas as pd
from matplotlib.pyplot import ylabel

from utils import mongo_utils

from utils.constants import PLOT_STYLE

from utils.constants import LOCATIONS, INDIC_URS, REV_INDIC_URS

enterprises = mongo_utils.find_all_enterprises_group_by_country()
countries = list(enterprises["country"].unique())
indic_urs = list(enterprises["indic_ur"].unique())
years = list(mongo_utils.find_all_years())

country_codes = mongo_utils.find_country_codes()
country_names = list(country_codes[country_codes["two_letter_code"].isin(countries)]["full_name"])


def country_wise_enterprise_count():
    return html.Div(
        id="country-enterprises-id",
        children=country_wise_enterprise_count_component(country_names[0], INDIC_URS[indic_urs[0]]),
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
        dcc.Dropdown(years, year, id='pie-country-selection-id', clearable=False),
        dcc.Graph(
            id='pie-country-enterprises-id-graph',
            figure=px.pie(
                df[["c_enterprises", "country"]].sort_values(by="c_enterprises", ascending=False).head(5),
                values='c_enterprises', names='country',
                title=f"Distribution of Companies across The Top 5 European Countries")
        )
    ]


def country_wise_enterprise_count_component(country_value, indic_ur):
    country = country_codes[country_codes["full_name"] == country_value]["two_letter_code"].iloc[0]
    enterprise_df = mongo_utils.find_enterprises_by_country_and_indic_ur(country, REV_INDIC_URS[indic_ur])
    if enterprise_df.empty:
        return [
            dcc.Dropdown(country_names, country_value, id='country-selection-id', clearable=False,),
            dcc.Dropdown(LOCATIONS, indic_ur, id='indic-selection-id', clearable=False,),
            dcc.Graph(
                id='country-enterprises-id-graph',
                figure=px.box(pd.DataFrame({"year": [], "c_enterprises": []}), x='year', y='c_enterprises',
                              title=f'No data present.Please select some other options."')
            )

        ]
    colors = enterprise_df['enterprises'].apply(lambda x: 'Projected' if x == 0 else 'Given')
    return [
        dcc.Dropdown(country_names, country_value, id='country-selection-id'),
        dcc.Dropdown(LOCATIONS, indic_ur, id='indic-selection-id'),
        dcc.Graph(
            id='country-enterprises-id-graph',
            figure=px.bar(enterprise_df[["c_enterprises", "year"]], x='year', y='c_enterprises',
                          title=f'Trend in Number of Companies in {country_value}', color=colors)
        )
    ]


def country_enterprises_year_bar_chart_component(year):
    enterprises_df = mongo_utils.find_all_by_country_year(year).sort_values(by="c_enterprises").tail(10)[::-1]
    return [
        dcc.Dropdown(years, year, id='year-selection-id', clearable=False,),
        dcc.Graph(
            id='enterprises-by-year-graph',
            figure=px.bar(enterprises_df, y='c_enterprises', x='country',
                          title=f'Distribution of Companies in Europe in Year {year}')
        )
    ]
