# from dash import Dash, dcc, html
# import plotly.express as px
# import pandas as pd
#
# # Sample data
# data = {
#     'Category': ['A', 'B', 'C', 'A', 'B', 'C'],
#     'Value1': [10, 15, 12, 18, 20, 16],
#     'Value2': [5, 8, 6, 9, 10, 8]
# }
# df = pd.DataFrame(data)
#
# # Initialize the Dash app
# app = Dash(__name__)
#
# # Define the layout of the dashboard
# app.layout = html.Div(children=[
#     html.H1(children='Multi-Chart Dashboard'),
#
#     html.Div(children=[
#         dcc.Graph(
#             id='bar-chart',
#             figure=px.bar(df, x='Category', y='Value1', title='Bar Chart')
#         )
#     ], style={'width': '48%', 'display': 'inline-block'}),
#
#     html.Div(children=[
#         dcc.Graph(
#             id='scatter-plot',
#             figure=px.scatter(df, x='Category', y='Value2', title='Scatter Plot')
#         )
#     ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),
#
#     html.Div(children=[
#         dcc.Graph(
#             id='line-chart',
#             figure=px.line(df, x='Category', y='Value1', title='Line Chart')
#         )
#     ], style={'width': '48%', 'display': 'inline-block'}),
#
#     html.Div(children=[
#         dcc.Graph(
#             id='pie-chart',
#             figure=px.pie(df, names='Category', values='Value2', title='Pie Chart')
#         )
#     ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
# ])
#
# # Run the app
# if __name__ == '__main__':
#     app.run(debug=True, port=8070)