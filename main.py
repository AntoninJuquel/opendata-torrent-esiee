import datetime
import time
import dash
from dash import State
from dash import dcc
from dash import html
from figures import get_bar_fig, get_geo_fig
from dash.dependencies import Input, Output
from progress import ProgressManager

from scrap import execute_scrapping
from multithreadcrawler import crawl_by_batch, purge_runs

from threading import Thread

red_button_style = {'background-color': 'red',
                    'color': 'white',
                    'height': '50px',
                    'width': '140px',
                    'margin-top': '50px',
                    'margin-left': '50px'}

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    html.Div([
        html.H4('Opendata Torrent'),
        html.Button(children='pause', id='pause-btn', n_clicks=0),
        html.Button(children='fetch new data', id='fetch-new-data-btn', n_clicks=0),
        html.Div(dcc.Input(id='num-of-torrent-input', type='text')),
        html.H6("Please enter the number of torrent you wish to scrape per category, then press on 'scrape new torrents'"),
        html.Button(children='scrape new torrents', id='scrape-new-torrents-btn', n_clicks=0),
        html.Button(children='purge data', id='purge-data-btn', n_clicks=0, style=red_button_style),
        html.Div(id='live-update-text'),
        html.Div(id='live-update-text-2'),
        dcc.Graph(id='live-update-graph'),
        dcc.Graph(id='live-update-map'),

        # useless text fields
        html.Div(id='live-update-text-3'),
        html.Div(id='live-update-text-4'),
        html.Div(id='live-update-text-5'),
        dcc.Interval(
            id='interval-component',
            interval=1*1000, # in milliseconds
            n_intervals=0,
            disabled=False
        )
    ])
)


@app.callback(Output('live-update-graph', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph_live(n):
    return update_bar_wrapped()


@app.callback(Output('live-update-map', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_map_live(n):
    return update_map_wrapped()

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
    Output('live-update-text-2', 'children'),
    Input('scrape-new-torrents-btn', 'n_clicks'),
    State('num-of-torrent-input', 'value'),
)
def scrape_torrent_files(n_clicks, value):
    if value is None:
        return ""
    if value.isnumeric():
        value = int(value)
        thread = Thread(target=execute_scrapping,args=(value,))
        thread.start()
        return "Scrapping {} files !".format(value * 8)
    return ""

@app.callback(
    Output('live-update-text-4', 'children'),
    Input('fetch-new-data-btn', 'n_clicks'),
)
def crawl_through_torrent_files(n_clicks):
    if n_clicks != 0:
        ProgressManager().create_progress("runs")
        thread = Thread(target=crawl_by_batch)
        thread.start()
    return ""


@app.callback(
    Output('live-update-text-3', 'children'),
    Input('num-of-torrent-input', 'value')
)
def print_num_of_torrents(value):
    if value is None:
        return ""
    if value.isnumeric():
        ProgressManager().write_line("This will fetch {} torrent files.".format(int(value) * 8))
        return ""

@app.callback(
    Output('live-update-text-5', 'children'),
    Input('purge-data-btn', 'n_clicks', ),
    prevent_initial_call=True
)
def purge_data_func(n_clicks):
    purge_runs()
    ProgressManager().write_line("Deleted the previous data !")
    return ""


@app.callback(Output('live-update-text', 'children'),
              Input('interval-component', 'n_intervals'))
def show_progress(n):
    text = ProgressManager().show()
    return text

def update_map_wrapped():
    try:
        return get_geo_fig()
    except:
        time.sleep(0.5)
        update_map_wrapped()

def update_bar_wrapped():
    try:
        return get_bar_fig()
    except:
        time.sleep(0.5)
        update_bar_wrapped()

if __name__ == '__main__':
    app.run_server(debug=True)
