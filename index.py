import dash
import dash_core_components as dcc
import dash_html_components as html
from app import server
from app import app
from dash.dependencies import Input, Output
from layouts import first_layout

# see https://dash.plot.ly/external-resources to alter header, footer and favicon
app.index_string = ''' 
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>MegaData Baseball-App</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
        </footer>
        <div>MegaData Baseball-App</div>
    </body>
</html>
'''


#app.layout = html.Div([
#    dcc.Location(id='url', refresh=False),
#    html.Div(id='page-content')
#])

app.layout = first_layout


# Update page
# # # # # # # # #
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/first_layout':
        return first_layout

if __name__ == '__main__':
    app.run_server(debug=True)