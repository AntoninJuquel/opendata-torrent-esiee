from logging import log
from os import name
from numpy import exp, log10, log2
from numpy.core.fromnumeric import size, sort
import pandas as pd
import plotly
import plotly.graph_objs as go
from plotly.offline import *
import plotly.express as px
import parse as ps
import country_converter as coco

#init_notebook_mode(connected=True)
def get_geo_fig():
  """
  Cette fonction va lire le json json/geo.json
  et va retourner figure plotly qui est une carte du monde
  """
  ps.parse("runs/")
  df = pd.read_json("json/geo.json")

  geo_data = []
  
  for data in df:
    for locations in df[data]["locs"]:
      lat_lng = locations.split(",")
      geo_data.append(go.Scattergeo(
            name=f"",
            text = f"{df[data]['size']} mo",
            lat = [lat_lng[0]],
            lon = [lat_lng[1]],
            marker = dict(
                size = log2(df[data]['size']),
                color = 'rgb(0,0,0)',
                line_color='rgb(255,255,255)',
                line_width=0.25,
                sizemode = 'area'
            )))

  if len(df) == 0:
    geo_data.append(go.Scattergeo())

  fig_title = 'Répartition des téléchargements de fichiers torrent dans le monde'
  layout = dict(title={'text':fig_title, 'x':0.5})
  fig = go.Figure(data=geo_data, layout=layout)
  return fig

def get_bar_fig():
  """
  Cette fonction va lire le json json/bar.json
  et va retourner un histogramme
  """
  ps.parse("runs/")
  df = pd.read_json("json/bar.json")

  bar_data = []
  
  for country in df:
      bar_data.append(go.Bar(name=country, 
                  x=df[country]["sizes"], y=df[country]["amounts"],
                  text=country, textposition='auto',
                  textfont=dict(color='white')))
  fig_title = 'Volume des téléchargements de fichiers torrent par taille (en mo) par pays'
  layout = dict(title={'text':fig_title, 'x':0.5},
                barmode='stack', 
                xaxis_title="Taille en mo",
                yaxis_title="Nombre de personnes",
              )

  fig = go.Figure(data=bar_data, layout=layout)
  return fig



if __name__ == '__main__':
  plotly.offline.plot(get_geo_fig(), filename='stackbar.html')
