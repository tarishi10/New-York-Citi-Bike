################################################ DIVVY BIKES DASHBOARD #####################################################

import streamlit as st
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl
from datetime import datetime as dt
from numerize.numerize import numerize
from PIL import Image


########################### Initial settings for the dashboard ##################################################################


st.set_page_config(page_title = 'Divvy Bikes Strategy Dashboard', layout='wide')
st.title("Divvy Bikes Strategy Dashboard")

# Define side-bar
st.sidebar.title("Aspect Selector")
page = st.sidebar.selectbox('Select an aspect of the analysis',
  ["Intro page","Weather component and bike usage",
   "Most popular stations",
    "Interactive map with aggregated bike trips", "Recommendations"])

st.markdown("The dashboard will help with the expansion problems Divvy currently faces")
st.markdown("Right now, Divvy bikes runs into a situation where customers complain about bikes not being avaibale at certain times. This analysis aims to look at the potential reasons behind this.")

########################## Import data ###########################################################################################

df = pd.read_csv('reduced_data_to_plot.csv', index_col = 0)
top20 = pd.read_csv('top20.csv', index_col = 0)
df_resampled=pd.read_csv('resampled_dua_linechart_data.csv',index_col=0)


#################################################Define the charts####################################################################

###### BAR CHART######
fig = go.Figure(go.Bar(x = top20['start_station_name'], y = top20['value'], marker={'color': top20['value'],'colorscale': 'Blues'}))
fig.update_layout(
    title = 'Top 20 most popular bike stations in New York',
    xaxis_title = 'Start stations',
    yaxis_title ='Sum of trips',
    width = 900, height = 600
)
st.plotly_chart(fig, use_container_width=True)


##### LINE CHART######
### use resampled data
fig_2 = make_subplots(specs = [[{"secondary_y": True}]])

fig_2.add_trace(
    go.Scatter(
        x=df['date'],
        y=df['bike_rides_daily'],
        name='Daily bike rides',
        line=dict(color='blue')   
    ),
    secondary_y=False
)

fig_2.add_trace(
    go.Scatter(
        x=df['date'],
        y=df['avgTemp'],
        name='Weekly temperature',
        line=dict(color='red')    
    ),
    secondary_y=True
)
fig.update_layout(
    title='Daily bikes and avgtemp in New York in 2022',
    xaxis_title='Date',
    yaxis_title='Sum of trips',
    width=900,
    height=600,
    yaxis=dict(
        title='Sum of trips',
        titlefont=dict(color='blue'),
        tickfont=dict(color='blue')
    ),
    yaxis2=dict(
        title='Avg Temperature (°C)',
        titlefont=dict(color='red'),
        tickfont=dict(color='red'),
        anchor='x',
        overlaying='y',
        side='right'
    )
)

st.plotly_chart(fig_2, use_container_width=True)


### Add the map ###

path_to_html = "NY_bike_trips_kepler_map.html" 

# Read file and keep in variable
with open(path_to_html,'r') as f: 
    html_data = f.read()

    ## Show in webpage
st.header("Aggregated Bike Trips in Nw York")
st.components.v1.html(html_data,height=1000)
