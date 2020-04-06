import dash_html_components as html
import dash_core_components as dcc

def Header():
    return html.Div([
        html.H1('MegaData'),
        get_menu()
    ], className="header")


def get_menu():
    menu = html.Div([
        dcc.Link('Players', href='/pages/player/'),
        "   |   ",
        dcc.Link('Compare', href='/pages/compare/'),
        "   |   ",
        dcc.Link('Squads', href='/pages/squads/'),
    ], className="row ")
    return menu