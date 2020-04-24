# resources:
# https://towardsdatascience.com/how-to-build-a-complex-reporting-dashboard-using-dash-and-plotl-4f4257c18a7f
# https://davidcomfort-dash-app1.herokuapp.com/cc-travel-report/paid-search/

# https://dash.plotly.com/layout
# https://github.com/davidcomfort/dash_sample_dashboard/blob/master/layouts.py
# 
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table as dt

from pymongo import MongoClient
import numpy as np 

from app import app
from .components import Header

client = MongoClient("localhost:27017")
db=client['baseballmd']
collection = db.players

rawPlayerData = pd.DataFrame(list(collection.find({},{"_id" : 0})))

'''
TO DO:
- Make table vertical
- Remove unecessary stuff from the table, Figure out what table lines mean
- Laying out the Page
    - Make dropdown shorter 
    - place picture and table right next to each other
- place second dropdwon right next to it
    - mirror player selection
'''

options = []
for name in rawPlayerData['fullName']:
    options.append(name)

# this is the layout
layout = html.Div([
    Header(),

    html.H3('Players Page'),
    dcc.Dropdown(
        id='app-1-dropdown',
        options=[
            {'label': '{}'.format(i), 'value': i} for i in options
        ],
        placeholder="Select Player",
    ),
    html.Div([ 
        html.Div(id='app-1-display-value'),
        html.Div(id='datatable-interactivity-container'),
    ]) 
], className="page")

# https://github.com/davidcomfort/dash_sample_dashboard/blob/master/callbacks.py
# https://dash.plotly.com/basic-callbacks

@app.callback(
    Output('datatable-interactivity-container', 'children'),
    [Input('app-1-dropdown', 'value')]
)
def update_styles(value):
    if value:
        myData = rawPlayerData.loc[rawPlayerData['fullName'] == 'Roger Bernadina']
        relevantData = myData.drop(columns = ['id', 'imageLink'])
        descriptionValues = []
        valuesValues = []
        for cName in relevantData.columns:
            descriptionValues.append(cName)
        for playerValue in relevantData.loc[0]:
            valuesValues.append(playerValue)
        d = {}
        d['Descriptions'] = descriptionValues
        d['Values'] = valuesValues
        pivotRelevant = pd.DataFrame(data=d)
        table = dt.DataTable(
            id='table',
            columns=[{"name": i, "id": i, "selectable": True} for i in pivotRelevant.columns],
            data=pivotRelevant.to_dict('records'),
            style_table={'overflowX': 'scroll', 'whitespace': "normal", 'height':'auto'},
            style_as_list_view=True,
            style_cell={'minWidth': '18px', 'width': '18px', 'maxWidth': '18px',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
            }
        )
        return table

@app.callback(
    Output('app-1-display-value', 'children'),
    [Input('app-1-dropdown', 'value')])
def display_value(value):
    if value:
        data = rawPlayerData.loc[rawPlayerData['fullName'] == value]
        playerImage = html.Img(src=data['imageLink'].iloc[0])
        return playerImage
    else:
        return 'no player selected'
