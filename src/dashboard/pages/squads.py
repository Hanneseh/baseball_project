import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import dash
import dash_table as dt
from pymongo import MongoClient
import numpy as np 
from app import app

client = MongoClient("localhost:27017")
db=client['baseballmd']
collection = db.players

rawPlayerData = pd.DataFrame(list(collection.find()))

'''
TO DO:
- Take the name from the dropdownlist, search his id in the dataframe
- Use the ID to querry MongoDB
    - Get all hitting carrer stats form the database for this player: 465668 and organize them in a datafram
    - Hints: {"id" : NumberInt(465668), "statGroupe" : "hitting"}
- display some data of the player from mongo db
- Define tow buttons: "batting", "Filding"
'''

options = []
for name in rawPlayerData['fullName']:
    options.append(name)

layout = html.Div([
    html.H3('This is the Squads Page'),

     dcc.Dropdown(
        id='app-1-dropdown',
        options=[
            {'label': '{}'.format(i), 'value': i} for i in options
        ],
        placeholder="Select Player" 
    ),
    html.Div(id='app-1-display-valueSquad')

], className="page")

@app.callback(
    Output('app-1-display-valueSquad', 'children'),
    [Input('app-1-dropdown', 'value')])
def display_value(value):
    if value:
        data = rawPlayerData.loc[rawPlayerData['fullName'] == value]
        playerImage = html.Img(src=data['imageLink'].iloc[0])
        return playerImage
    else:
        return 'no player selected'