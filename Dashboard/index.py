import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from pages.database import getDBRefreshInfo

from app import app
from pages import mainPage, squads

# get database refresh info
updateInfo = getDBRefreshInfo()

# root app layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.Div(id="navLinkDiv", style={"display":"None"}),
                    html.Div([updateInfo], id="dbRefreshInfo", style={"float":"left", "font-size":"small","color":"whitesmoke"}, title="This shows the last date when the database was refreshed"),
                ], className="row "),
            ],className="placeHolderDiv"),
        ], className="backgroundDiv"),
    ], className="header"),
    html.Div(id='page-content')
], className = "rootPage")

app.title = 'NL Baseball'

# callback for returning the correct layout depending on url
@app.callback(
    [Output('page-content', 'children'),
    Output('navLinkDiv', 'children')],
    [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/nlbaseball/':
        return mainPage.layout, dcc.Link('Squads', href='/nlbaseball/',style={'color': '#0580FF'}, id='navLink')
    elif pathname == '/pages/squads/':
        return squads.layout, dcc.Link('Players', href='/pages/player/',style={'color': '#0580FF'}, id='navLink')
    else:
        return '404','404'

# start the dashboard
if __name__ == '__main__':
    app.run_server(host="0.0.0.0", debug=True)
    
