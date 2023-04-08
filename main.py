import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, callback, Output, Input

df = pd.read_csv('epoch_csv.csv')
date_format = '%b %d, %Y'

app = Dash(__name__)

app.layout = html.Div([
    dcc.RangeSlider(
        min=0,
        max=len(df) - 1,
        tooltip={"placement": "bottom", "always_visible": True},
        step=1,
        marks=None,
        updatemode='drag',
        value=[0, len(df) - 1],
        id='my-range-slider'),
    html.Div(html.B(id='display-selected-range')),
    dcc.Graph(id='my-graph')
])


@callback(
    [Output('my-graph', 'figure'),
     Output('display-selected-range', 'children')],
    [Input('my-range-slider', 'value')]
)
def update_graph(value):
    start_index = value[0]
    end_index = value[1]
    filtered_df = df.iloc[start_index:end_index + 1][:].reset_index(drop=True)
    filtered_df['timestamp'] = pd.to_datetime(filtered_df['timestamp'], unit='s')
    line_graph = px.line(filtered_df, x='timestamp', y='some_data')

    start_date = filtered_df['timestamp'][0].strftime(date_format)
    end_date = filtered_df['timestamp'].iloc[-1].strftime(date_format)
    range_div = f'Selected Range: {start_date} to {end_date}'
    return line_graph, range_div


if __name__ == '__main__':
    app.run_server(debug=True)
