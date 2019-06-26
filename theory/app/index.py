import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from theory.app.app import app
from theory.app.pages import debugging
from theory.app.pages import header

app.layout = html.Div([
    header.get_header(),
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
], className='container')

@app.callback(Output('page-content', 'children'),
              [Input('menu-tabs', 'value')])
def display_page(tab_value):
    print('Current tab:', tab_value)
    if (tab_value == 'debug') or (tab_value == 'tabs'):
        return debugging.layout
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True)
