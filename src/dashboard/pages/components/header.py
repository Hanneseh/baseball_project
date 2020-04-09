import dash_html_components as html
import dash_core_components as dcc

def Header():
    return html.Div([
        html.H1('Baseball'),
        get_menu()
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