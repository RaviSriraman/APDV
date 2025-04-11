from dash import Dash, dcc, callback, Output, Input, html
import dash_bootstrap_components as dbc
import plotly.express as px

import utils.mongo_utils as mongo_utils
import utils.sql_db_utils  as sql_utils
from pages.main import dashboard
import pandas as pd
from dotenv import load_dotenv


@callback(
    Output('year-wise-enterprise-count-id', 'children'),
    Input('year-selection-id', 'value')
)
def update_city_wise_enterprise_count(year):
    all_enterprises = mongo_utils.find_all_enterprises()
    enterprises_df = (all_enterprises[all_enterprises["year"] == year].groupby(by=["country", "year"])
                        .agg({'enterprises': 'sum'})
                        .sort_values(by="enterprises").reset_index())
    enterprises_df = enterprises_df[enterprises_df["enterprises"] > 0]
    return [
        dcc.Dropdown(all_enterprises["year"].unique(), year, id='year-selection-id'),
        dcc.Graph(
            id='enterprises-by-year-graph',
            figure=px.bar(enterprises_df, y='enterprises', x='country',
                          title=f'Enterprises in top countries in year {year}')
        )
    ]


@callback(
    Output('city-enterprises-id', 'children'),
    Input('city-selection', 'value')
)
def update_city_wise_enterprise_count(city_value):
    all_enterprises = mongo_utils.find_all_enterprises()
    enterprise_df = mongo_utils.find_enterprises_by_city(city_value)
    enterprises_by_city = enterprise_df.groupby(by=["year", "city"]).agg(
        {'enterprises': 'sum'}).reset_index()
    all_enterprises = all_enterprises[all_enterprises["enterprises"] > 0]
    df = enterprises_by_city[enterprises_by_city["enterprises"] > 0 ]
    return [
        dcc.Dropdown(all_enterprises["city"].unique(), city_value, id='city-selection'),
        dcc.Graph(
            id='city-enterprises-id-graph',
            figure=px.bar(df[["enterprises", "year"]], x='year', y='enterprises',
                          title=f'Enterprises in {city_value}')
        )
    ]

@callback(
    Output('country-enterprises-id', 'children'),
    Input('country-selection-id', 'value')
)
def update_country_wise_enterprise_count(country_value):
    all_enterprises = mongo_utils.find_all_enterprises()
    enterprise_df = mongo_utils.find_enterprises_by_county(country_value)
    enterprises_by_country = enterprise_df.groupby(by=["year", "country"]).agg(
        {'enterprises': 'sum'}).reset_index()
    enterprises_by_country = enterprises_by_country[enterprises_by_country["enterprises"] > 0]
    return [
        dcc.Dropdown(all_enterprises[all_enterprises["enterprises"] > 0]["country"].unique(), country_value, id='country-selection-id'),
        dcc.Graph(
            id='country-enterprises-id-graph',
            figure=px.bar(enterprises_by_country[["enterprises", "year"]], x='year', y='enterprises',
                          title=f'Enterprises in {country_value}')
        )
    ]

@callback(
    Output('map-year-wise-enterprise-count-id', 'children'),
    Input('map-year-selection-id', 'value')
)
def update_europe_country_wise_enterprise_count(year):
    all_enterprises = mongo_utils.find_all_enterprises()
    enterprise_df = mongo_utils.find_enterprises_by_year(year)
    enterprises_by_country = enterprise_df.groupby(by=["country"]).agg(
        {'enterprises': 'sum'}).reset_index()

    enterprises_by_country = enterprises_by_country[enterprises_by_country["enterprises"] > 0]
    country_codes: pd.DataFrame = mongo_utils.find_country_codes().rename(columns={"two_letter_code": "country"})
    new_df = pd.merge(enterprises_by_country, country_codes, on=["country"])

    return [
            dcc.Dropdown(all_enterprises["year"].unique(), year, id='map-year-selection-id'),
            dcc.Graph(
                id='map-enterprises-by-year-graph',
                figure=px.choropleth(new_df, locations="three_letter_code",
                        color="enterprises",
                        hover_name="country",
                        scope="europe",
                        color_continuous_scale=px.colors.sequential.Plasma)
            )
        ]


# Run the app
if __name__ == '__main__':
    load_dotenv()
    title = dcc.Markdown("Impact of Tourism on Enterprises", className="bg-light", style={"font-size": 30})
    app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    list_of_tabs = [
        dbc.Tab(
            dbc.Card(
                [
                    dbc.CardBody(
                        [
                            dashboard()
                        ]
                    )
                ]
            ),
            label="Enterprises",
            activeLabelClassName="bg-light",
        ),
        dbc.Tab(
            dbc.Card(
                [
                    dbc.CardBody(
                        [
                            html.Div(sql_utils.fetch_by_year(2012).__str__())

                        ]
                    )
                ]
            ),
            label="Tourism",
            activeLabelClassName="bg-light",
        ),
        dbc.Tab(
            dbc.Card(
                [
                    dbc.CardBody(
                        [
                            html.Div("")
                        ]
                    )
                ]
            ),
            label="Enterprises Tourism",
            activeLabelClassName="bg-light",
        )
    ]

    app.layout = dbc.Container(
        [
            dbc.Row([
                dbc.Col([title], width=12, style={"text-align": "center", "margin": "auto"})
            ]),

            dbc.Tabs(list_of_tabs)
        ]
    )
    app.run(debug=True, port=8070, host="0.0.0.0")
