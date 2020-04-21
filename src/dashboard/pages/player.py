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
import dash_table


from pymongo import MongoClient
import numpy as np 


from app import app
from .components import Header

client = MongoClient("localhost:27017")

db=client.baseballmd
result=db.players.count_documents({})

cursor = db.players # choosing the collection you need

df = pd.DataFrame.from_records(cursor.find())

df
#this needs to be edited to the right directory of your computer

#app=dash.Dash(__name__)

# this is the layout
layout = html.Div([
    Header(),

    html.H3('Players Page'),
    dcc.Dropdown(
        id='app-1-dropdown',
        options=[
            {'label': 'Player - {}'.format(i), 'value': i} for i in [
                'Player 1','Player 2', 'Player 3', 'player 4'
            ]
        ],
        placeholder="Select Player" 
    ),
"""
    dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name": i, "id": i, "deletable": True, "selectable": True} for i in df.columns
        ],
        data=df.to_dict('records'),
        style_table={'overflowX': 'scroll', 'whiteSpace': 'normal', 'height':'auto'},
        editable=True,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        row_selectable="multi",
        row_deletable=True,
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current= 0,
        page_size= 10,
    ),
    html.Div(id='datatable-interactivity-container')
"""
], className="page")

# https://github.com/davidcomfort/dash_sample_dashboard/blob/master/callbacks.py
# https://dash.plotly.com/basic-callbacks

@app.callback(
    Output('datatable-interactivity', 'style_data_conditional'),
    [Input('datatable-interactivity', 'selected_columns')]
)
def update_styles(selected_columns):
    return [{
        'if': { 'column_id': i },
        'background_color': '#D2F3FF'
    } for i in selected_columns]


@app.callback(
    Output('app-1-display-value', 'children'),
    [Input('app-1-dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)
