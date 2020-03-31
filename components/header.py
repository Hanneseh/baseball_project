import dash_html_components as html
import dash_core_components as dcc

def Header():
    return html.Div([
        get_header()
    ])

def get_header():
    header = html.Div([
        html.Div([
            html.H5(
                'MegaData Header')
        ])
    ])
    return header