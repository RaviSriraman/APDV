from dash import Dash, dcc, html
import plotly.express as px
import pandas as pd

import os
from pymongo import MongoClient

client = MongoClient(os.getenv("MONGO_DB_URI"))
apdv_db = client["APDV"]
collection = apdv_db["enterprises"]

enterprise_df = pd.DataFrame(collection.find())

countries_local_enterprises = enterprise_df[enterprise_df["indic_ur"] == "EC2039V"].groupby(by="country").agg(
    {'enterprises': 'sum'}).reset_index()

countries_local_enterprises = countries_local_enterprises.sort_values(by="enterprises", ascending=True).tail(10)[::-1]

cities_local_enterprises = enterprise_df[enterprise_df["indic_ur"] == "EC2039V"].groupby(by=["country", "city", "year"]).agg(
    {'enterprises': 'sum'}).reset_index()

cities_local_enterprises = cities_local_enterprises.sort_values(by="enterprises", ascending=False).head(10)

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

    html.Div(children=[
        dcc.Graph(
            id='enterprises-bar-chart2',
            figure=px.bar(cities_local_enterprises, x='enterprises', y='city',
                          title='Enterprises in top cities')
        )
    ], style={'width': '48%', 'display': 'inline-block'}),

])

# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=8070, host="0.0.0.0")
