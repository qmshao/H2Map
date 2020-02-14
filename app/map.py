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


import json
import requests
import dash_dangerously_set_inner_html
import numpy as np

import lib.userComponent as userComp


# Load and Preprocess Data
with open('StationInfo3.json', 'r') as f:
    stationInfo = json.load(f)    

numStation = len(stationInfo['name'])


typeList = {}


for i in range(numStation):
    Type = stationInfo['type'][i]
    if not (Type in typeList):
        typeList[Type] = [i]
    else:
        typeList[Type].append(i)

stationInfo['lat'] = np.array(stationInfo['lat'])
stationInfo['lon'] = np.array(stationInfo['lon'])
stationInfo['name'] = np.array(stationInfo['name'])



app = dash.Dash(
    __name__,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)



# Map
defaultSelected = ['open','development','bus']
fig = userComp.generateMap(stationInfo, typeList, defaultSelected)



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
            # id = "app-container",
            id = "h2station-container",
            # style={"width": "100%","height":"100%", "background-color": "rgba(255, 255, 255, 0.01)"},
            # style={"width": "100%","height":"80%", "padding": "2em"},
            children = [
                html.Div(
                    id = "h2station-map-container",
                    # style={"width": "60%","height":"50em","float":"left", "display":"block","padding": "1em"},
                    children = [
                        dcc.Graph(id="station-map"),
                        userComp.generateFilter(defaultSelected),
                        userComp.generateModal()
                    ],
                ),
                html.Div(
                    id = "h2station-info" ,
                    # className = "row",
                    # style = {"width": "35%",  "height": "50em","float":"left","padding": "1em","overflow-y": "auto","overflow-x": "hidden"}, #"overflow-y": "scroll",
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

        info = [ 
            dash_dangerously_set_inner_html.DangerouslySetInnerHTML(stationInfo['html'][index]),
            userComp.makeDashTable(stationInfo['table'][index])
        ]

    else:
        info = staticIntro
    return info

@app.callback(
    Output("station-map", "figure"),
    [dash.dependencies.Input('map-filter', 'value')])
def updateMap(selected):
    return userComp.generateMap(stationInfo, typeList, selected)

# ======= Callbacks for modal popup =======
# @app.callback(
#     Output("markdown", "style"),
#     [Input("h2station-info", "n_clicks"), Input("markdown_close", "n_clicks")],
# )
# def update_click_output(button_click, close_click):
#     ctx = dash.callback_context

#     if ctx.triggered:
#         prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
#         if prop_id == "h2station-info":
#             return {"display": "block"}

#     return {"display": "none"}

# Running the server
if __name__ == "__main__":
    app.run_server(debug=False, host='0.0.0.0')