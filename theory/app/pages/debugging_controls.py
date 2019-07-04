import dash_html_components as html
import dash_core_components as dcc

component_controls = html.Div([
        html.H6('Component'),
        dcc.RadioItems(
            options=[
                {'label': 'Axial', 'value': 'axial'},
                {'label': 'Tangential', 'value': 'tangential'},
            ],
            value='axial',
            id='component-selector',
            className='btn-group',
            labelClassName='btn btn-secondary'
        ),
    ],
    className="d-flex flex-column",
),

pipe_controls = html.Div([
        html.H6('Pipe', className='p-1 m-0',),
        html.Div(
            [
                html.Div(
                    [
                        html.Label("rho", id="pipe-rho-title", className="column"),
                        dcc.Input(
                            id="pipe-rho-input",
                            value=7200,
                            type='number',
                            className="m-1", style={'width': '90px'},
                        ),
                    ],
                ),
                html.Div(
                    [
                        html.Label("alpha", id="pipe-alpha-title", className="column"),
                        dcc.Input(
                            id="pipe-alpha-input",
                            value=4875,
                            type='number',
                            className="m-1", style={'width': '90px'},
                        ),
                    ],
                ),
                html.Div(
                    [
                        html.Label("beta", id="pipe-beta-title", className="column"),
                        dcc.Input(
                            id="pipe-beta-input",
                            value=2368,
                            type='number',
                        className="m-1", style={'width': '90px'},
                        ),
                    ],
                ),
                html.Div(
                    [
                        html.Label("Rb", id="pipe-rb-title", className="column"),
                        dcc.Input(
                            id="pipe-rb-input",
                            value=.16,
                            type='number',
                            className="m-1", style={'width': '90px'},
                        ),
                    ],
                ),
            ],
            className="d-flex flex-row",
        ),
    ],
    className="d-flex flex-column m-1"
),

rock_controls = html.Div([
        html.H6('Rock', className='p-1 m-0',),
        html.Div(
            [
                html.Div(
                    [
                        html.Label("rho", id="rho-title", className="column"),
                        dcc.Slider(
                            id="rho-slider",
                            min=1000,
                            max=3000,
                            step=100,
                            value=1500,
                            className="column",
                        ),
                    ],
                    className="ml-auto p-1", style={'width': '200px'},
                ),
                html.Div(
                    [
                        html.Label("alpha", id="alpha-title", className="column"),
                        dcc.Slider(
                            id="alpha-slider",
                            min=1000,
                            max=9000,
                            step=100,
                            value=1500,
                            className="column",
                        ),
                    ],
                    className="ml-auto p-1", style={'width': '200px'},
                ),
                html.Div(
                    [
                        html.Label("beta", id="beta-title", className="column"),
                        dcc.Slider(
                            id="beta-slider",
                            min=500,
                            max=9000,
                            step=100,
                            value=1500,
                            className="column",
                        ),
                    ],
                    className="ml-auto p-1", style={'width': '200px'},
                ),
                html.Div(
                    [
                        html.Label(
                            "window", id="window-title", className="column"
                        ),
                        dcc.Slider(
                            id="window-slider",
                            min=10,
                            max=200,
                            step=10,
                            value=30,
                            className="column",
                        ),
                    ],
                    className="ml-auto p-1", style={'width': '200px'},
                ),
            ],
            className="d-flex flex-wrap",
        ),
    ],
    className="d-flex flex-column m-1"
),
