import dash_html_components as html
import dash_core_components as dcc

def Header():
    return html.Div([
        html.Div([
            html.H1('vdsak'),
            get_menu(),
        ], className="backgroundDiv"),
    ], className="header")


def get_menu():
    menu = html.Div([
        dcc.Link('Players', href='/pages/player/',style={'color': 'black'}),
        "   |   ",
        dcc.Link('Compare', href='/pages/compare/',style={'color': 'black'}),
        "   |   ",
        dcc.Link('Squads', href='/pages/squads/',style={'color': 'black'}),
    ], className="row ")
    return menu