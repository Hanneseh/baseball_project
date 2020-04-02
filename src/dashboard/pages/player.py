import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from .components import Header

layout = html.Div([
    Header(),

    html.H3('This is the Player Page'),
    dcc.Dropdown(
        id='app-1-dropdown',
        options=[
            {'label': 'Player - {}'.format(i), 'value': i} for i in [
                'August','Hannes', 'Marcus', 'Basit'
            ]
        ]
    ),
    html.Div(id='app-1-display-value'),
], className="page")


@app.callback(
    Output('app-1-display-value', 'children'),
    [Input('app-1-dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)