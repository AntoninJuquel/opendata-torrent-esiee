from os import name
from numpy.core.fromnumeric import size, sort
import pandas as pd
import plotly
import plotly.graph_objs as go
from plotly.offline import *
import plotly.express as px
import parse as ps

init_notebook_mode(connected=True)

# json_file = ps.parse("runs/")
df = pd.read_json("final.json")

data = [
#   go.Histogram(x=[(100, 200, 200),(199,299,299)]),
# go.Histogram(x=[(200, 200, 200),(299,299,299)]),
#   go.Histogram(x=[(100, 200, 200),(199,299,299)])

]

# for country in df:
#   x0 = []
#   x1 = []
#   sizes = df[country]["sizes"]
#   amounts = df[country]["amounts"]
#   for i in range(len(sizes)):
#     sizeint = int(float(sizes[i]))
#     hundreds = sizeint-sizeint%100
#     for j in range(amounts[i]):
#       x0.append(hundreds)
#       x1.append(hundreds+99)
#   x = [tuple(x0), tuple(x1)]
#   data.append(go.Histogram(x=x, name=country))


def sizeToIntervalStr(size):
  sizeint = int(float(size))
  hundreds = sizeint-sizeint%100
  return f"{hundreds} - {hundreds + 99}"

for country in df:
    data.append(go.Bar(name=country, 
	               x=[sizeToIntervalStr(size) for size in df[country]["sizes"]], y=df[country]["amounts"],
	               text=country, textposition='auto',
	               textfont=dict(color='white')))
fig_title = 'Torrent'
layout = dict(title={'text':fig_title, 'x':0.5},
              barmode='stack', 
              # xaxis=dict(tickmode='linear'),
              xaxis_title="Taille en mo",
                yaxis_title="Nombre de personnes",
              )

fig = go.Figure(data=data, layout=layout)

plotly.offline.plot(fig, filename='stackbar.html')