from dash import Dash, dcc, html, callback, Output, Input
import plotly.express as px
import pandas as pd

import os
from pymongo import MongoClient

client = MongoClient(os.getenv("MONGO_DB_URI"))
apdv_db = client["APDV"]
collection = apdv_db["enterprises"]

enterprise_df = pd.DataFrame(collection.find())

countries_local_enterprises = enterprise_df.groupby(by=["country", "year"]).agg(
    {'enterprises': 'sum'}).reset_index()

countries_local_enterprises = countries_local_enterprises.sort_values(by="enterprises", ascending=True)

cities_local_enterprises = enterprise_df.groupby(by=[ "year", "city"]).agg(
    {'enterprises': 'sum'}).reset_index()

cities_local_enterprises = cities_local_enterprises.sort_values(by=["enterprises"], ascending=False)

# Initialize the Dash app
app = Dash(__name__)

# Define the layout of the dashboard
app.layout = html.Div(children=[
    html.H1(children='European Tourism and Enterprises'),
    html.Div(children=[
        dcc.Graph(
            id='enterprises-bar-chart',
            figure=px.bar(countries_local_enterprises, x='enterprises', y='country',
                          title='Enterprises in top countries')
        )
    ], style={'width': '48%', 'display': 'inline-block'}),

    html.Div(
        id="city-enterprises-id",
        children=[
        dcc.Dropdown(cities_local_enterprises["city"].unique(), 'FR', id='city-selection'),
        dcc.Graph(
            id='enterprises-bar-chart2',
            figure=px.bar(cities_local_enterprises[["enterprises", "year"]], x='year', y='enterprises',
                          title='Enterprises in top cities')
        )
    ], style={'width': '48%', 'display': 'inline-block'}),

    html.Div(
        id="country-enterprises-id",
        children=[
        dcc.Dropdown(countries_local_enterprises["country"].unique(), 'FR', id='country-selection-id'),
        dcc.Graph(
            id='country-enterprises-id-graph',
            figure=px.bar(countries_local_enterprises[["enterprises", "year"]], x='year', y='enterprises',
                          title='Enterprises in top cities')
        )
    ], style={'width': '48%', 'display': 'inline-block'}),

])

@callback(
    Output('city-enterprises-id', 'children'),
    Input('city-selection', 'value')
)
def update_graph(value):
    dff = cities_local_enterprises[cities_local_enterprises.city==value]
    dff = dff[dff["enterprises"] > 0]
    return [
        dcc.Dropdown(enterprise_df["city"].unique(), value, id='city-selection'),
        dcc.Graph(
            id='enterprises-bar-chart2',
            figure=px.bar(dff[["enterprises", "year"]], x='year', y='enterprises',
                          title='Enterprises in top cities')
        )
    ]

@callback(
    Output('country-enterprises-id', 'children'),
    Input('country-selection-id', 'value')
)
def update_country_graph(value):
    dff = countries_local_enterprises[countries_local_enterprises.country==value]
    dff = dff[dff["enterprises"] > 0]
    return [
        dcc.Dropdown(countries_local_enterprises[countries_local_enterprises["enterprises"] > 0]["country"].unique(), value, id='country-selection-id'),
        dcc.Graph(
            id='country-enterprises-id-graph',
            figure=px.bar(dff[["enterprises", "year"]], x='year', y='enterprises',
                          title='Enterprises in top countries')
        )
    ]

# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=8070, host="0.0.0.0")
