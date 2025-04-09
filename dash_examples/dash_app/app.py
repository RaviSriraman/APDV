from dash import Dash, html, dcc

app = Dash(__name__)

plot_file = "/shared/plot.html"

app.layout = html.Div([
    html.H1("Live Sales Visualization"),
    html.Iframe(srcDoc=open(plot_file).read(), width="100%", height="600px")
])

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050)
