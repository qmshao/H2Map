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
import re
import requests
import dash_dangerously_set_inner_html

with open('StationList.json', 'r') as f:
    stations = json.load(f)    

stationInfo = {}
stationInfo['name'] = []
stationInfo['lat'] = []
stationInfo['lon'] = []
stationInfo['id'] = []

lat0 = 0
lon0 = 0

for s in stations:
    name = re.search(r'title:(.*?)]', s['opts']['title']).group(1)
    Id =  re.search(r'station:(.*?),', s['opts']['title']).group(1).strip()
    stationInfo['name'].append(name)
    stationInfo['id'].append(Id)
    stationInfo['lat'].append(s['latitude'])
    stationInfo['lon'].append(s['longitude'])

    

    lat0 += s['latitude']
    lon0 += s['longitude']

lat0 /= len(stationInfo['name'])
lon0 /= len(stationInfo['name'])

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
    print(clickPt)
    if (clickPt):
        index = clickPt['points'][0]['pointIndex']
        Id = stationInfo['id'][index]
        print(Id)
        res = json.loads(requests.get('https://cafcp.org/cafcp-station-details/'+Id).text)
        info =dash_dangerously_set_inner_html.DangerouslySetInnerHTML(res['node_view'])

    else:
        info = staticIntro




    return info



# Running the server
if __name__ == "__main__":
    app.run_server(debug=True)