#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 11:38:43 2020

@author: QuanMin
"""
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import plotly.graph_objs as go

import json
import requests
import dash_dangerously_set_inner_html

with open('StationInfo.json', 'r') as f:
    stationInfo = json.load(f)    



lat0 = (max(stationInfo['lat']) + min(stationInfo['lat']))/2
lon0 = (max(stationInfo['lon']) + min(stationInfo['lon']))/2

# print(stationLatitude)



app = dash.Dash(
    __name__,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)


# Map
trace = go.Scattermapbox(
# trace = go.Choroplethmapbox(    
    lat=stationInfo['lat'],
    lon=stationInfo['lon'],
    mode="markers",
    marker = dict(
        size = 15,
    ),
    hovertext=stationInfo['name'],
    # color_discrete_sequence=["fuchsia"], 
    # zoom=3, 
    # height=300,
)


layout = go.Layout(
    mapbox_style="open-street-map",
    margin={"r":0,"t":0,"l":0,"b":0},
    mapbox = dict(
        zoom=5,
        center=dict(lat=lat0,lon=lon0)
    )
)

fig = go.Figure(data=[trace], layout=layout)

# Static Intro
staticIntro =  dcc.Markdown(
    '''
        # Map Test 

        This is a Demo for interactive map
    '''
)



            

app.layout = html.Div(
    # className = "container scalable twelve columns",
    id = "big-app-container",
    children = [
        html.Div(
            id="banner",
            className="banner",
            children=[
                html.Div(
                    id="banner-text",
                    children=[
                        html.H5("Interactive Map Demo"),
                        html.H6("This is a Demo for H2 Station Map Test"),
                    ],
                ),
            ],
        ),
        html.Div(
            className = "view view-h2stationmaps-v2 view-id-h2stationmaps_v2 view-display-id-page",
            # style={"width": "100%","height":"100%", "background-color": "rgba(255, 255, 255, 0.01)"},
            style={"width": "100%","height":"80%", "padding": "2em"},
            children = [
                html.Div(
                    # id = "station-map",
                    style={"width": "60%","height":"50em","float":"left", "display":"block","padding": "1em"},
                    children = dcc.Graph(id="station-map", figure=fig, style={"height":"100%"}),
                ),
                html.Div(
                    id = "h2station-info" ,
                    # className = "row",
                    style = {"width": "35%",  "height": "50em","float":"left","padding": "1em","overflow-y": "auto","overflow-x": "hidden"}, #"overflow-y": "scroll",
                    children = html.Div(
                        className = "node-wrapper",
                        id = "station-info" ,
                        children = staticIntro,
                    ),
                ),
            ],
        ),
    ]
    
)




@app.callback(
    Output("station-info", "children"),
    [
        Input("station-map", "clickData"),
    ],
)
def updateStationInfo(clickPt):
    if (clickPt):
        index = clickPt['points'][0]['pointIndex']
        print(stationInfo['name'][index] + ' clicked')
        info =dash_dangerously_set_inner_html.DangerouslySetInnerHTML(stationInfo['html'][index])

    else:
        info = staticIntro




    return info



# Running the server
if __name__ == "__main__":
    app.run_server(debug=False, host='0.0.0.0')