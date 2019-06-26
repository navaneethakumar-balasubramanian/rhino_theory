import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = [
    "https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"
]

app = dash.Dash(external_stylesheets=external_stylesheets, static_folder='assets')

app.config.suppress_callback_exceptions = True
