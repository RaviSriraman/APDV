from dash import Dash, dcc, callback, Output, Input
import plotly.express as px

import utils.mongo_utils as mongo_utils
from pages.main import dashboard

# df = px.data.tips()
#
# @callback(
#     Output("graph", "figure"),
#     Input("names", "value"),
#     Input("values", "value"),
# )
# def generate_chart(names, values):
#     fig = px.pie(df, values=values, names=names, hole=0.3)
#     return fig


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


# Run the app
if __name__ == '__main__':
    app = Dash(__name__)
    app.layout = dashboard()
    app.run(debug=True, port=8070, host="0.0.0.0")
