import datetime
import dash
from dash import State
import dash_core_components as dcc
import dash_html_components as html
import plotly
from app import get_bar_fig, get_geo_fig
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app = dash.Dash(__name__)
app.layout = html.Div(
    html.Div([
        html.H4('Opendata Torrent'),
        html.Button(children='pause', id='pause-btn', n_clicks=0),
        html.Button(children='fetch new data', id='fetch-new-data-btn', n_clicks=0),
        html.Div(dcc.Input(id='num-of-torrent-input', type='text')),
        html.Button(children='scrape new torrents', id='scrape-new-torrents-btn', n_clicks=0),
        html.Div(id='live-update-text'),
        dcc.Graph(id='live-update-graph'),
        dcc.Graph(id='live-update-map'),
    html.Div(dcc.Input(id='input-on-submit', type='text')),
    html.Div(id='container-button-basic',
             children='Enter a value and press submit'),
        dcc.Interval(
            id='interval-component',
            interval=1*1000, # in milliseconds
            n_intervals=0,
            disabled=False
        )
    ])
)

i = 1

@app.callback(Output('live-update-text', 'children'),
              Input('interval-component', 'n_intervals'))
def update_metrics(n):
    global i
    i+=1
    return [
            i,
    ]

@app.callback(Output('live-update-graph', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph_live(n):
    return get_bar_fig()

@app.callback(Output('live-update-map', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_map_live(n):
    return get_geo_fig()

# button

@app.callback(
    Output('interval-component', 'disabled'),
    Output('pause-btn', 'children'),
    Input('pause-btn', 'n_clicks')
)
def pause_play(n_clicks):
    if n_clicks % 2 == 0:
        return False, "Pause"
    else :
        return True, "Play"


@app.callback(
    Input('scrape-new-torrents-btn', 'n_clicks'),
    State('num-of-torrent-input', 'value')
)
def scrape_torrent_files(value):
    if value.isnumeric():
        value = int(value)
        execute_scrapping(value)


if __name__ == '__main__':
    app.run_server(debug=True)
