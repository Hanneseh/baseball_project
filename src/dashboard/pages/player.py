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

from app import app
from .components import Header



#this needs to be edited to the right directory of your computer
df= pd.read_csv('/Users/Hannes/baseball-project/baseballmd/src/dashboard/pages/datacsv/notebooks_playerStats.csv')
df
df2=pd.read_csv('/Users/Hannes/baseball-project/baseballmd/src/dashboard/pages/datacsv/data19.csv')
#app=dash.Dash(__name__)

# this is the layout
layout = html.Div([
    Header(),

    html.H3('Players'),
    dcc.Dropdown(
        id='app-1-dropdown',
        options=[
            {'label': 'Player - {}'.format(i), 'value': i} for i in [
                'August','Hannes', 'Marcus', 'Basit'
            ]
        ],
        placeholder="Select Player" 
    ),
    html.Div(id='app-1-display-value'),

    html.Div(dash_table.DataTable(
    id='table2',
    columns=[{"name": i, "id":i} for i in df.columns],
    data=df.to_dict("rows"),
    style_table={'overflowX': 'scroll'},

    
)),
    html.Div(dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id":i} for i in df2.columns],
    data=df2.to_dict("rows"),
    style_table={'overflowX': 'scroll'},
  

    
))


], className="page")



# https://github.com/davidcomfort/dash_sample_dashboard/blob/master/callbacks.py
# https://dash.plotly.com/basic-callbacks

@app.callback(
    Output('app-1-display-value', 'children'),
    [Input('app-1-dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)