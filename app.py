import pandas as pd
import plotly
import plotly.graph_objs as go
from plotly.offline import *
import plotly.express as px
import parse as ps
import flag

init_notebook_mode(connected=True)

# json_file = ps.parse("runs/")
df = pd.read_json("final.json")

data = []
for country in df:
    data.append(go.Bar(name=country, 
	               x=df[country]["sizes"], y=df[country]["amounts"],
	               text=flag.flag(country), textposition='auto',
	               textfont=dict(color='white')))
fig_title = 'Torrent'
layout = dict(title={'text':fig_title, 'x':0.5},
              barmode='stack', 
              xaxis=dict(tickmode='linear'),
              xaxis_title="Taille en mo",
                yaxis_title="Nombre de personnes",
              )
print(data)
fig = go.Figure(data=data, layout=layout)

plotly.offline.plot(fig, filename='stackbar.html')