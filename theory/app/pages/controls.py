import dash_html_components as html
import dash_core_components as dcc

from theory.app.pages import css

pegleg = html.Div([
    html.H6('Pegleg Effect'),
        html.Div(
            [
                html.Div(
                    [
                        html.Label("RC", id="pegleg-rc-title", className="column"),
                        dcc.Input(
                            id="pegleg-rc-input",
                            value=-.357,
                            type='number',
                            className="m-1",
                            style={'width': '70px', 'height': '20px'},
                        ),
                    ],
                ),
                html.Div(
                    [
                        html.Label("delay (ms)", id="pegleg-delay-title", className="column"),
                        dcc.Input(
                            id="pegleg-delay-input",
                            value=1.6,
                            type='number',
                            className="m-1",
                            style={'width': '70px', 'height': '20px'},
                        ),
                    ],
                ),
                html.Div([
                        dcc.Checklist(
                            options=[
                                {'label': 'Add Pegleg Effect', 'value': 'add-pegleg'},
                            ],
                            value=['add-pegleg'],
                            id='pegleg-controls',
                        )
                    ],
                    className='m-1 d-flex flex-row',
                )
            ],
            className="d-flex flex-row",
            style=css.box_control,
        ),
    ],
    className="d-flex flex-column m-1"
)

window_controls = [
        html.Label(
            "window", id="window-title",
        ),
        html.Div([
                dcc.Slider(
                    id="window-slider",
                    min=10,
                    max=1000,
                    step=10,
                    value=650,
                ),
            ],
            style={'width': '200px'},
            className='m-1'
        ),
]

gain_controls = [
        html.Label(
            "gain", id="gain-title",
        ),
        html.Div([
                dcc.Slider(
                    id="gain-slider",
                    min=10,
                    max=750,
                    step=10,
                    value=30,
                ),
            ],
            style={'width': '200px'},
            className='m-1'
        ),
]

debugger_controls = html.Div([
        html.H6('Plot'),
        html.Div(
            [
                *window_controls,
                html.Div([
                        dcc.Checklist(
                            options=[
                                {'label': 'Hide Frequency Domain', 'value': 'hide-complex'},
                            ],
                            value=[],
                            id='debugger-controls',
                        )
                    ],
                    className='m-1 d-flex flex-row',
                )
            ],
            className="d-flex flex-row",
            style=css.box_control,
        ),
    ],
    className='d-flex flex-column'
)

explore_controls = html.Div([
        html.H6('Plot'),
        html.Div(
            [
                *window_controls,
                *gain_controls,
            ],
            className="d-flex flex-row",
            style=css.box_control,
        ),
    ],
    className='d-flex flex-column'
)

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
            labelClassName='btn btn-secondary',
            labelStyle={'background-color': '#699869'}
        ),
    ],
    className="d-flex flex-column",
    style={'width': '200px'},
),

wavelet_controls = html.Div([
        html.H6('Wavelet'),
        dcc.RadioItems(
            options=[
                {'label': 'Primary', 'value': 'primary'},
                {'label': 'Reflected', 'value': 'reflected'},
                {'label': 'Multiple', 'value': 'multiple'},
            ],
            value='primary',
            id='wavelet-selector',
            className='btn-group',
            labelClassName='btn btn-secondary',
            labelStyle={'background-color': '#3c73a5'}
        ),
    ],
    className="d-flex flex-column ml-2",
),


def bandpass_inputs():
    inputs = []
    defaults = [40, 50, 200, 240]
    for i, d in zip(range(1, 5), defaults):
        name = 'bpf{}'.format(str(i))
        inputs.append(html.Div(
            [
                html.Label("corner {}".format(str(i)), id=name, className="column"),
                dcc.Input(
                    id=name,
                    value=d,
                    type='number',
                    className="m-1",
                    style={'width': '70px', 'height': '20px'},
                ),
            ],
        ),)
    return inputs

filter_controls = html.Div([
        html.H6('Trapezoidal Bandpass Filter', className='p-1 m-0',),
        html.Div(
            bandpass_inputs(),
            className="d-flex flex-row",
            style=css.box_control,
        ),
    ],
    className="d-flex flex-column m-1",
    id='filters',
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
                            className="m-1",
                            style={'width': '70px', 'height': '20px'},
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
                            className="m-1",
                            style={'width': '70px', 'height': '20px'},
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
                        className="m-1",
                        style={'width': '70px', 'height': '20px'},
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
                            className="m-1",
                            style={'width': '70px', 'height': '20px'},
                        ),
                    ],
                ),
            ],
            className="d-flex flex-row",
            style=css.box_control,
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
            ],
            className="d-flex flex-wrap",
            style=css.box_control,
        ),
    ],
    className="d-flex flex-column m-1"
),


def rho_inputs():
    inputs = []
    for i in range(1):
        inputs.append(
            dcc.Input(
                id="rho-input-{}".format(i+1),
                value=2250 + i * 750,
                type='number',
                className="p-1 m-1",
                style={'width': '70px', 'height': '20px'},
            ),
        )
    return inputs

rock_range_controls = html.Div([
        html.H6('Rock', className='p-1 m-0',),
        html.Div(
            [
                html.Div(
                    [
                            html.Div([
                                    html.Label("velocity", id="velocity-range-title", className="mt-2 mr-2"),
                                    html.Div([
                                        dcc.RangeSlider(
                                                id="velocity-range-slider",
                                                min=500,
                                                max=5000,
                                                step=100,
                                                value=[1500, 3000],
                                                pushable=1000,
                                            ),
                                        ],
                                        style={'width': '200px'},
                                        className='mt-1',
                                    ),
                                    html.Label("step:", className="mt-1 mr-1 ml-1"),
                                    dcc.Input(
                                        id="velocity-step-input",
                                        value=500,
                                        type='number',
                                        className="p-1 m-1",
                                        style={'width': '60px', 'height': '20px'},
                                    ),
                            html.Div([
                                html.Label("rho:", id="rho-range-title", className="mr-1"),
                                *rho_inputs()
                            ], className='m-1'),
                            ],
                            className='d-flex flex-row',
                        ),
                    ],
                    className="d-flex flex-row",
                ),
            ],
            style=css.box_control,
        ),
    ],
)
