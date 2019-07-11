import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.plotly as py
import plotly.graph_objs as go
from plotly import tools

import numpy as np

from theory.core import Pipe, Rock, TheoreticalWavelet
from theory.app.app import app
from theory.app.pages.controls import (
    rock_controls, pipe_controls, component_controls,
    debugger_controls, filter_controls)

from scipy import signal

layout = html.Div(
    [
        html.Div([
            *component_controls,
            debugger_controls,
            *pipe_controls,
            *rock_controls,
            *filter_controls,
            ],
            className='d-flex flex-wrap'
        ),
        html.Div(
            [
                html.Div(dcc.Graph(id="wavelets", animate=False)),
            ],
            className="d-inline-flex flex-wrap",
        ),
    ]
)

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
        Input("pipe-alpha-input", "value"),
        Input("pipe-rho-input", "value"),
        Input("pipe-beta-input", "value"),
        Input("pipe-rb-input", "value"),
        Input("debugger-controls", "value"),
        Input("bpf1", "value"),
        Input("bpf2", "value"),
        Input("bpf3", "value"),
        Input("bpf4", "value"),
    ],
)
def update_figure(alpha, rho, beta, window, component, pipe_alpha, pipe_rho, pipe_beta, pipe_rb, debugger_controls, bpf1, bpf2, bpf3, bpf4):

    if 'hide-complex' in debugger_controls:
        hide_complex = True
        specs=[
            [{"colspan": 2, "rowspan": 1}, None, {"colspan": 2, "rowspan": 1}, None, {"colspan": 2, "rowspan": 1}, None],
            [{"colspan": 2, "rowspan": 1}, None, {"colspan": 2, "rowspan": 1}, None, {"colspan": 2, "rowspan": 1}, None],
            [{"colspan": 2, "rowspan": 1}, None, {"colspan": 2, "rowspan": 1}, None, {"colspan": 2, "rowspan": 1}, None],
        ]
        subplot_titles=(
            "Full Primary Wavelet (time)",
            "Full Reflected Wavelet (time)",
            "Full Multiple Wavelet (time)",
            "Primary Wavelet (time)",
            "Reflected Wavelet (time)",
            "Multiple Wavelet (time)",
            "Filtered Primary Wavelet (time)",
            "Filtered Reflected Wavelet (time)",
            "Filtered Multiple Wavelet (time)",
        )
    else:
        hide_complex = False
        specs=[
            [{"colspan": 3}, None, None, {"colspan": 3}, None, None],
            [{"colspan": 3}, None, None, {"colspan": 3}, None, None],
            [{"colspan": 2, "rowspan": 1}, None, {"colspan": 2, "rowspan": 1}, None, {"colspan": 2, "rowspan": 1}, None],
            [{"colspan": 2, "rowspan": 1}, None, {"colspan": 2, "rowspan": 1}, None, {"colspan": 2, "rowspan": 1}, None],
            [{"colspan": 2, "rowspan": 1}, None, {"colspan": 2, "rowspan": 1}, None, {"colspan": 2, "rowspan": 1}, None],
        ]
        subplot_titles=(
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
            "Filtered Primary Wavelet (time)",
            "Filtered Reflected Wavelet (time)",
            "Filtered Multiple Wavelet (time)",
        )

    pipe = Pipe(Ro=0.1365, Ri=0.0687, Rb=pipe_rb, alpha=pipe_alpha, rho=pipe_rho, beta=pipe_beta)
    rock = Rock(alpha, rho, beta)
    wavelet = TheoreticalWavelet(pipe, rock, component=component, filterby=[bpf1, bpf2, bpf3, bpf4])

    frequency_domain_primary = wavelet.primary_in_frequency_domain_complex
    frequency_domain_reflected = wavelet.reflected_in_frequency_domain_complex

    if not hide_complex:

        primary_real = go.Scatter(x=wavelet.frequencies, y=frequency_domain_primary.real, marker=dict(color="red"))
        primary_imag = go.Scatter(x=wavelet.frequencies, y=frequency_domain_primary.imag, marker=dict(color="red"))
        reflected_real = go.Scatter(
            x=wavelet.frequencies, y=frequency_domain_reflected.real, marker=dict(color="green")
        )
        reflected_imag = go.Scatter(
            x=wavelet.frequencies, y=frequency_domain_reflected.imag, marker=dict(color="green")
        )

    primary_wavelet_full = go.Scatter(
        y=wavelet.primary_in_time_domain(None), marker=dict(color="red")
    )
    reflected_wavelet_full = go.Scatter(
        y=wavelet.reflected_in_time_domain(None), marker=dict(color="green")
    )
    multiple_wavelet_full = go.Scatter(
        y=wavelet.multiple_in_time_domain(None), marker=dict(color="blue")
    )


    time_sampling_window = wavelet.get_time_range_for_window(window)

    primary_wavelet = go.Scatter(
        x=time_sampling_window,
        y=wavelet.primary_in_time_domain(window, filtered=False),
        marker=dict(color="red"),
    )
    reflected_wavelet = go.Scatter(
        x=time_sampling_window,
        y=wavelet.reflected_in_time_domain(window, filtered=False),
        marker=dict(color="green"),
    )
    multiple_wavelet = go.Scatter(
        x=time_sampling_window,
        y=wavelet.multiple_in_time_domain(window, filtered=False),
        marker=dict(color="blue"),
    )

    filtered_primary_wavelet = go.Scatter(
        x=time_sampling_window,
        y=wavelet.primary_in_time_domain(window, filtered=True),
        marker=dict(color="red"),
    )
    filtered_reflected_wavelet = go.Scatter(
        x=time_sampling_window,
        y=wavelet.reflected_in_time_domain(window, filtered=True),
        marker=dict(color="green"),
    )
    filtered_multiple_wavelet = go.Scatter(
        x=time_sampling_window,
        y=wavelet.multiple_in_time_domain(window, filtered=True),
        marker=dict(color="blue"),
    )

    fig = tools.make_subplots(
        rows=5 if not hide_complex else 5-2,
        cols=6,
        specs=specs,
        subplot_titles=subplot_titles,
    )

    if not hide_complex:
        fig.append_trace(primary_real, 1, 1)
        fig.append_trace(primary_imag, 1, 4)
        fig.append_trace(reflected_real, 2, 1)
        fig.append_trace(reflected_imag, 2, 4)

    start_row = 3 if not hide_complex else 1

    fig.append_trace(primary_wavelet_full, start_row, 1)
    fig.append_trace(reflected_wavelet_full, start_row, 3)
    fig.append_trace(multiple_wavelet_full, start_row, 5)

    fig.append_trace(primary_wavelet, start_row + 1, 1)
    fig.append_trace(reflected_wavelet, start_row + 1, 3)
    fig.append_trace(multiple_wavelet, start_row + 1, 5)

    fig.append_trace(filtered_primary_wavelet, start_row + 2, 1)
    fig.append_trace(filtered_reflected_wavelet, start_row + 2, 3)
    fig.append_trace(filtered_multiple_wavelet, start_row + 2, 5)

    height = 1000 if not hide_complex else 500
    fig["layout"].update(height=height, width=1100, showlegend=False, template="seaborn")
    return fig
