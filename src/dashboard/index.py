# run this file by navigating to it in the terminal and then do 
# python index.py
# to start the dashboard
# to stop the dashboard type this in ther terminal:
# ctrl+c

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from pages import player, squads

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.Div(id="navLinkDiv"),
                ], className="row "),
            ],className="placeHolderDiv"),
        ], className="backgroundDiv"),
    ], className="header"),
    html.Div(id='page-content')
], className = "rootPage")

@app.callback(
    [Output('page-content', 'children'),
    Output('navLinkDiv', 'children')],
    [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/pages/player/':
        return player.layout, dcc.Link('Squads', href='/pages/squads/',style={'color': 'whitesmoke'}, id='navLink')
    elif pathname == '/pages/squads/':
        return squads.layout, dcc.Link('Players', href='/pages/player/',style={'color': 'whitesmoke'}, id='navLink')
    else:
        return '404','404'

if __name__ == '__main__':
    app.run_server(debug=True)
    
