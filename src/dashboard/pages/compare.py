import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
from app import app
from .components import Header
import dash_table
import plotly.express as px
df3= pd.read_csv('/Users/Hannes/baseball-project/baseballmd/src/dashboard/pages/datacsv/notebooks_playerStats.csv')

'''
TO DO:
- Get all carrer summary stats form the database and organize them in a datafram
    - Hints: {"type" : "career", "statGroupe" : "hitting"}
- Try to figure a way out 
'''

#https://dash.plotly.com/dash-core-components/graph

df4 = pd.DataFrame(dict(
    r=[914, 542, 228, 14, 107],
    theta=['Games played','Runs','doubles',
           'triples', 'Homeruns']))

df5 = pd.DataFrame(dict(
    r=[375, 241, 92, 18, 54],
    theta=['Games played','Runs','doubles',
           'triples', 'Homeruns']))

#df6 = 
    #r=df3[],
    #theta=['Games played','Runs','doubles',
           #'triples', 'Homeruns']))


fig = px.line_polar(df4, r='r', theta='theta', line_close=True, width=500, height=500)
fig2 = px.line_polar(df5, r='r', theta='theta', line_close=True, width=500, height=500)
layout = html.Div([
    Header(),
    html.H3('Compare Players'),


    # dash_table.DataTable(
    #     id='datatable-interactivity',
    #     columns=[
    #         {"name": i, "id": i, "deletable": True, "selectable": True} for i in df3.columns
    #     ],
    #     data=df3.to_dict('records'),
    #     #style_cell={'padding': '5px',
    #      #               'whiteSpace': 'no-wrap',
    #       #              'overflow': 'hidden',
    #        #             
    #         #            'maxWidth': 0,
    #          #           'height': 30,
    #           #          'textAlign': 'left'},
    #     style_table={'overflowX': 'scroll', 'whiteSpace': 'normal', 'height':'auto'},
    #     editable=True,
    #     filter_action="native",
    #     sort_action="native",
    #     sort_mode="multi",
    #     column_selectable="single",
    #     row_selectable="multi",
    #     row_deletable=True,
    #     selected_columns=[],
    #     selected_rows=[],
    #     page_action="native",
    #     page_current= 0,
    #     page_size= 10,
    # ),
    # html.Div(id='datatable-interactivity-container'),

    # html.Div([dcc.Graph(figure=fig)], style={'float':'left'}),
    # html.Div([dcc.Graph(figure=fig2)], style={'float':'right'})
    



], className="page")
