import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from .components import Header

layout = html.Div([
    Header(),
    html.H3('This is the Compare Page'),
], className="page")