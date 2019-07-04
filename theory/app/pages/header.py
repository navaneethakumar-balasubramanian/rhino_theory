import dash
import dash_core_components as dcc
import dash_html_components as html

from theory.app.app import app

def get_menu():
    menu = dcc.Tabs(id='menu-tabs', value='tabs', children=[
        dcc.Tab(label='Debug', value='debug'),
        dcc.Tab(label='Explore', value='explore'),
    ],)
    return menu

def get_logo():
    return html.Img(src=app.get_asset_url('logo.svg'), height='60px',
                    style={'margin-right': '1%'})

def get_header():
    return html.Div([
        get_logo(),
        get_menu(),
    ], className='row', style={'padding': '1%'})
