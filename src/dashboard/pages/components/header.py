# import dash_html_components as html
# import dash_core_components as dcc

# def Header():
#     return html.Div([
#         html.Div([
#             html.Div([
#                 get_menu(),
#             ],className="placeHolderDiv"),
#         ], className="backgroundDiv"),
#     ], className="header")


# @app.callback(Output('page-content', 'children'),
# [Input('url', 'pathname')])
# def get_menu():
#     menu = html.Div([
#         dcc.Link('Players', href='/pages/player/',style={'color': 'black'}),
#         "   |   ",
#         dcc.Link('Squads', href='/pages/squads/',style={'color': 'black'}),
#     ], className="row ")
#     return menu

