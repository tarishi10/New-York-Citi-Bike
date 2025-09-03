################################################ CITI BIKES DASHBOARD #####################################################

import streamlit as st
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
#from streamlit_keplergl import keplergl_static
# from keplergl import KeplerGl
from datetime import datetime as dt
from numerize.numerize import numerize
from PIL import Image


########################### Initial settings for the dashboard ##################################################################


st.set_page_config(page_title = 'Citi Bikes Strategy Dashboard', layout='wide')
st.title("Citi Bikes Strategy Dashboard")

# Define side-bar
st.sidebar.title("Aspect Selector")
page = st.sidebar.selectbox('Select an aspect of the analysis',
["Intro page","Weather component and bike usage",
"Most popular stations",
"Interactive map with aggregated bike trips", "Recommendations"])


########################## Import data ###########################################################################################

df = pd.read_csv('reduced_data_to_plot.csv', index_col = 0)
top20 = pd.read_csv('top20.csv', index_col = 0)


### Intro page
if page == "Intro page":
    st.markdown("#### This dashboard aims at providing helpful and actionable insights on the business strategy and expansion of New York's Citi Bikes bike sharing service.")
    st.markdown("Right now, Citi Bikes runs into a situation where customers complain about bikes not being available at certain times. This analysis will look at the potential reasons behind this. The dashboard is separated into 4 sections: ")
    st.markdown("- Most popular stations")
    st.markdown("- Weather component and bike usage")
    st.markdown("- Interactive map with aggregated bike trips")
    st.markdown("- Recommendations")
    st.markdown("The dropdown menu on the left 'Aspect Selector' will take you to the different aspects of the analysis our team looked at.")
    
   # myImage = Image.open("bike.jpeg") #source: unsplash.com
   # st.image(myImage)



###### Page 2: Weather component and bike usage ############
### Create the dual axis line chart page ###
    
elif page == 'Weather component and bike usage':
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
    fig_2.update_layout(
        title='Daily bikes and avgtemp in New York in 2022',
        xaxis_title='Date',
        yaxis_title='Sum of trips',
        width=900,
        height=600,
        yaxis=dict(
            title='Sum of trips',
         #   titlefont=dict(color='blue'),
            tickfont=dict(color='blue')
        ),
        yaxis2=dict(
            title='Avg Temperature (°C)',
          #  titlefont=dict(color='red'),
            tickfont=dict(color='red'),
            anchor='x',
            overlaying='y',
            side='right'
        )
    )

    st.plotly_chart(fig_2, use_container_width=True)
    st.markdown("There is an obvious correlation between the rise and drop of temperatures and their relationship with the frequency of bike trips taken daily. As temperatures plunge, so does bike usage. This insight indicates that the shortage problem may be prevalent merely in the warmer months, approximately from May to October.")



##### Page 3: Most popular stations ####
 # Create the season variable

elif page == 'Most popular stations':
    
    # Create the filter on the side bar
    
    with st.sidebar:
        season_filter = st.multiselect(label= 'Select the season', options=df['season'].unique(),
    default=df['season'].unique())

    df.columns = df.columns.str.strip()
    
  #  df1 = df.query('season == @season_filter')
    df1 = df[df['season'].isin(season_filter)]
    
  # Define the total rides
    total_rides = float(df1['bike_rides_daily'].count())    
    st.metric(label = 'Total Bike Rides', value= numerize(total_rides))


###### BAR CHART######
    
    df1['value'] = 1 
    df_groupby_bar = df1.groupby('start_station_name')['value'].sum().reset_index()
    
    top_20 = df_groupby_bar.nlargest(20, 'value')
    fig = go.Figure(go.Bar(x = top_20['start_station_name'], y = top_20['value'], marker={'color': top_20['value'],'colorscale': 'Blues'}))
    fig.update_layout(
        title = 'Top 20 most popular bike stations in New York',
        xaxis_title = 'Start stations',
        yaxis_title ='Sum of trips',
        width = 900, height = 600
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("From the bar-chart it is clear that there are some start stations that are more popular than others - in the top 3 we can see W 21 St & 6 Ave, West St & Chambers St, Broadway & W 58 St. However, after the top 5 popular stations, there is not a huge difference between the other stations in the plot, indicating that there are clear preferences for the leading stations. This is a finding that we could cross-reference with the interactive map that you can access through the side bar select box.")


###### Page 4: Interactive map #####
elif page == 'Interactive map with aggregated bike trips': 

### Add the map ###
    st.write("Interactive map showing aggregated bike trips over New York city")
    path_to_html = "NY_bike_trips_kepler_map.html" 

# Read file and keep in a variable
    with open(path_to_html,'r') as f: 
        html_data = f.read()

    ## Show in webpage
    st.header("Aggregated Bike Trips in Nw York")
    st.components.v1.html(html_data,height=1000)
    st.markdown("#### Using the filter on the left hand side of the map we can check whether the most popular start stations also appear in the most popular trips.")
    st.markdown("The most popular start stations are:")
    st.markdown("W 21 St & 6 Ave, West St & Chambers St,and Broadway & W 58 St. While having the aggregated bike trips filter enabled, we can see that he West St and Bradway stations are the most popular start stations, and also account for the most commonly taken trips.")


####### Page 5: Recommendation #####
else:
    
    st.header("Conclusions and recommendations")
    bikes = Image.open("Bike love.jpeg")  #source: Unsplash
    st.image(bikes)
    st.markdown("### Our analysis has shown that Citi Bikes should focus on the following objectives moving forward:")
    st.markdown("- Add more stations to the locations around the West street avenue and Broadway street. These are the most popular start stations and routes taken. ")
    st.markdown("- Ensure that bikes are fully stocked in all these stations during the warmer months in order to meet the higher demand, but provide a lower supply in winter and late autumn to reduce logistics costs")