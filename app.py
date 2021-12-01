from os import name
from numpy.core.fromnumeric import size, sort
import pandas as pd
import plotly
import plotly.graph_objs as go
from plotly.offline import *
import plotly.express as px
import parse as ps
import country_converter as coco

init_notebook_mode(connected=True)
def get_geo_fig():
  ps.parse("runs/")
  df = pd.read_json("final.json")

  geo_data = []
  
  for country in df:
      for i in range(len(df[country]["sizes"])):
        index = len(df[country]["sizes"]) - i - 1
        geo_data.append(go.Scattergeo(
            name=df[country]["amounts"][index],
            locationmode = 'ISO-3',
            locations = [coco.convert(names=[f"{country}"], to='ISO3')],
            text =  df[country]["sizes"][index],
            marker = dict(
                size = index * 10,
                color = f'rgb({index * 255 / len(df[country]["sizes"])},0,0)',
                line_color='rgb(255,255,255)',
                line_width=0.25,
                sizemode = 'area'
            )))
  fig_title = 'Torrent'
  layout = dict(title={'text':fig_title, 'x':0.5},
                barmode='stack', 
                xaxis_title="Taille en mo",
                yaxis_title="Nombre de personnes",
              )

  fig = go.Figure(data=geo_data, layout=layout)
  return fig

def get_bar_fig():
  ps.parse("runs/")
  df = pd.read_json("final.json")

  bar_data = []
  

  for country in df:
      bar_data.append(go.Bar(name=country, 
                  x=df[country]["sizes"], y=df[country]["amounts"],
                  text=country, textposition='auto',
                  textfont=dict(color='white')))
  fig_title = 'Torrent'
  layout = dict(title={'text':fig_title, 'x':0.5},
                barmode='stack', 
                xaxis_title="Taille en mo",
                yaxis_title="Nombre de personnes",
              )

  fig = go.Figure(data=bar_data, layout=layout)
  return fig



if __name__ == '__main__':
  plotly.offline.plot(get_bar_fig(), filename='stackbar.html')
