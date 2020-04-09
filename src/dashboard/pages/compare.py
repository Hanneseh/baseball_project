import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
from app import app
from .components import Header
import dash_table
import plotly.express as px
df3= pd.read_csv('/Users/Hannes/baseball-project/baseballmd/src/dashboard/pages/datacsv/notebooks_playerStats.csv')


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
 
    

    html.Div(dash_table.DataTable(
    id='table3',
    columns=[{"name": i, "id":i} for i in df3.columns],
    data=df3.to_dict("rows"),
    style_table={'overflow': 'scroll'},
    )),

    html.Div([dcc.Graph(figure=fig)], style={'float':'left'}),
    html.Div([dcc.Graph(figure=fig2)], style={'float':'right'})
    
    

], className="page")
