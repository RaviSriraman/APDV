import threading
from time import sleep

from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
from flask_cors import CORS
from dagster import asset

@asset
def dash_2():
    df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')
    app = Dash()
    server = app.server
    CORS(server)
    app.layout = [
        html.H1(children='Title of Dash App', style={'textAlign': 'center'}),
        dcc.Dropdown(df.country.unique(), 'Canada', id='dropdown-selection'),
        dcc.Graph(id='graph-content')
    ]

    @callback(
        Output('graph-content', 'figure'),
        Input('dropdown-selection', 'value')
    )
    def update_graph(value):
        dff = df[df.country == value]
        return px.line(dff, x='year', y='pop')
    # threading.Thread(target= lambda : app.run(port=8060))
    app.run(port=8060)

if __name__=='__main__':
    dash_2()

