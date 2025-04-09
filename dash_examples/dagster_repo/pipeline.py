from dagster import job, op
import pandas as pd
import plotly.express as px

@op
def generate_data():
    df = pd.DataFrame({
        "date": pd.date_range("2023-01-01", periods=10),
        "sales": [100, 120, 90, 130, 110, 150, 170, 180, 160, 175],
    })
    return df

@op
def create_plot(data: pd.DataFrame):
    fig = px.line(data, x="date", y="sales", title="Sales Over Time")
    fig.write_html("/shared/plot.html")
    return "/shared/plot.html"

@job()
def build_visualization():
    create_plot(generate_data())
