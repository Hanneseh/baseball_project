# run this file by navigating to it in the terminal and then do 
# python index.py
# to start the dashboard
# to stop the dashboard type this in ther terminal:
# ctrl+c

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from pages import player, compare, squads

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/pages/player/':
        return player.layout
    elif pathname == '/pages/compare/':
        return compare.layout
    elif pathname == '/pages/squads/':
        return squads.layout
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True)