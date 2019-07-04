import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.plotly as py
import plotly.graph_objs as go
from plotly import tools

import numpy as np

from theory import Pipe, Rock, TheoreticalWavelet
from theory.app.app import app


# def get_layout_by_component(component='axial'):
#     if component == 'axial':
#         velocity = 'alpha'
#     else:
#         velocity == 'beta'

layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        html.Div([
                                html.Label('Component'),
                                dcc.RadioItems(
                                    options=[
                                        {'label': 'Axial', 'value': 'axial'},
                                        {'label': 'Tangential', 'value': 'tangential'},
                                    ],
                                    value='axial',
                                    id='component-selector',
                                ),
                            ],
                            className="col-sm",
                        ),
                        html.Div(
                            [
                                html.H5("rho", id="rho-title", className="column"),
                                dcc.Slider(
                                    id="rho-slider",
                                    min=1000,
                                    max=3000,
                                    step=100,
                                    value=1500,
                                    className="column",
                                ),
                            ],
                            className="col-sm",
                        ),
                        html.Div(
                            [
                                html.H5("alpha", id="alpha-title", className="column"),
                                dcc.Slider(
                                    id="alpha-slider",
                                    min=1000,
                                    max=9000,
                                    step=100,
                                    value=1500,
                                    className="column",
                                ),
                            ],
                            className="col-sm",
                        ),
                        html.Div(
                            [
                                html.H5("beta", id="beta-title", className="column"),
                                dcc.Slider(
                                    id="beta-slider",
                                    min=500,
                                    max=9000,
                                    step=100,
                                    value=1500,
                                    className="column",
                                ),
                            ],
                            className="col-sm",
                        ),
                        html.Div(
                            [
                                html.H5(
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
                            className="col-sm",
                        ),
                    ],
                    className="row",
                ),
            ]
        ),
        html.Div(
            [
                html.Div(dcc.Graph(id="wavelets", animate=False), className="col-sm"),
                # html.Div(dcc.Graph(id='reflected'), className="col-sm"),
                # html.Div(dcc.Graph(id='multiple'), className="col-sm")
            ],
            className="row",
        ),
    ])


@app.callback(
    dash.dependencies.Output("rho-title", "children"),
    [dash.dependencies.Input("rho-slider", "value")],
)
def update_rho_title(value):
    return "rho: {}".format(str(value))


@app.callback(
    dash.dependencies.Output("alpha-title", "children"),
    [dash.dependencies.Input("alpha-slider", "value")],
)
def update_alpha_title(value):
    return "alpha: {}".format(str(value))

@app.callback(
    dash.dependencies.Output("beta-title", "children"),
    [dash.dependencies.Input("beta-slider", "value")],
)
def update_alpha_title(value):
    return "beta: {}".format(str(value))

@app.callback(
    dash.dependencies.Output("window-title", "children"),
    [dash.dependencies.Input("window-slider", "value")],
)
def update_window_title(value):
    return "window: {}".format(str(value))


@app.callback(
    Output("wavelets", "figure"),
    [
        Input("alpha-slider", "value"),
        Input("rho-slider", "value"),
        Input("beta-slider", "value"),
        Input("window-slider", "value"),
        Input("component-selector", "value"),
    ],
)
def update_figure(alpha, rho, beta, window, component):

    j = np.arange(10001) + 1
    f = (j - 1) * 0.5

    pipe = Pipe(Ro=0.1365, Ri=0.0687, Rb=0.16, alpha=4875, rho=7800, beta=2368)
    rock = Rock(alpha, rho, beta)
    wavelet = TheoreticalWavelet(pipe, rock, frequencies=f, component=component)

    frequency_domain_primary = wavelet.make_symmetry_on_complex(wavelet.primary_in_frequency_domain_complex)
    frequency_domain_reflected = wavelet.make_symmetry_on_complex(wavelet.reflected_in_frequency_domain_complex)

    frequencies_trace = go.Scatter(y=f, mode="lines", marker=dict(color="black"))

    primary_real = go.Scatter(y=frequency_domain_primary.real, marker=dict(color="red"))
    primary_imag = go.Scatter(y=frequency_domain_primary.imag, marker=dict(color="red"))
    reflected_real = go.Scatter(
        y=frequency_domain_reflected.real, marker=dict(color="green")
    )
    reflected_imag = go.Scatter(
        y=frequency_domain_reflected.imag, marker=dict(color="green")
    )

    # primary_nyquist = go.Scatter(
    #     x=frequency_domain_primary.real,
    #     y=frequency_domain_primary.imag,
    #     marker=dict(color="red"),
    # )
    # reflected_nyquist = go.Scatter(
    #     x=frequency_domain_reflected.real,
    #     y=frequency_domain_reflected.imag,
    #     marker=dict(color="green"),
    # )

    primary_wavelet_full = go.Scatter(
        y=wavelet.primary_in_time_domain(None), marker=dict(color="red")
    )
    reflected_wavelet_full = go.Scatter(
        y=wavelet.reflected_in_time_domain(None), marker=dict(color="green")
    )
    multiple_wavelet_full = go.Scatter(
        y=wavelet.multiple_in_time_domain(None), marker=dict(color="blue")
    )

    time_sampling_window = (
        np.arange(
            0 - (window / 2 * wavelet.time_sampling),
            0 + (window / 2 * wavelet.time_sampling) + wavelet.time_sampling,
            wavelet.time_sampling,
        )
        * 1000
    )

    primary_wavelet = go.Scatter(
        x=time_sampling_window,
        y=wavelet.primary_in_time_domain(window),
        marker=dict(color="red"),
    )
    reflected_wavelet = go.Scatter(
        x=time_sampling_window,
        y=wavelet.reflected_in_time_domain(window),
        marker=dict(color="green"),
    )
    multiple_wavelet = go.Scatter(
        x=time_sampling_window,
        y=wavelet.multiple_in_time_domain(window),
        marker=dict(color="blue"),
    )

    fig = tools.make_subplots(
        rows=6,
        cols=6,
        specs=[
            [{"colspan": 1, "rowspan": 1}, None, None, None, None, None],
            [{"colspan": 3}, None, None, {"colspan": 3}, None, None],
            [{"colspan": 3}, None, None, {"colspan": 3}, None, None],
            [{"colspan": 2, "rowspan": 1}, None, {"colspan": 2, "rowspan": 1}, None, {"colspan": 2, "rowspan": 1}, None],
            [{"colspan": 2, "rowspan": 2}, None, {"colspan": 2, "rowspan": 2}, None, {"colspan": 2, "rowspan": 2}, None],
            [None, None, None, None, None, None],
        ],
        subplot_titles=(
            "Frequency Plot",
            "Primary - Real (freq)",
            "Primary - Imag (freq)",
            "Reflected - Real (freq)",
            "Reflected - Imag (freq)",
            "Full Primary Wavelet (time)",
            "Full Reflected Wavelet (time)",
            "Full Multiple Wavelet (time)",
            "Primary Wavelet (time)",
            "Reflected Wavelet (time)",
            "Multiple Wavelet (time)",
        ),
    )

    fig.append_trace(frequencies_trace, 1, 1)
    fig.append_trace(primary_real, 2, 1)
    fig.append_trace(primary_imag, 2, 4)
    fig.append_trace(reflected_real, 3, 1)
    fig.append_trace(reflected_imag, 3, 4)
    fig.append_trace(primary_wavelet_full, 4, 1)
    fig.append_trace(reflected_wavelet_full, 4, 3)
    fig.append_trace(multiple_wavelet_full, 4, 5)
    fig.append_trace(primary_wavelet, 5, 1)
    fig.append_trace(reflected_wavelet, 5, 3)
    fig.append_trace(multiple_wavelet, 5, 5)

    fig["layout"].update(height=1000, width=1000, showlegend=False, template="seaborn")

    return fig
