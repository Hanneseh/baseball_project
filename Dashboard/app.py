import dash

# instantiates the dashboard

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, url_base_pathname='/nlbaseball/')
server = app.server
app.scripts.config.serve_locally=True
app.config.suppress_callback_exceptions = True