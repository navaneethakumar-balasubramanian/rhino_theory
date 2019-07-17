import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.plotly as py
import plotly.graph_objs as go
from plotly import tools

import matplotlib.pyplot as plt

import numpy as np

from theory.core import Pipe, Rock, TheoreticalWavelet
from theory.app.app import app
from theory.app.pages.controls import component_controls, pipe_controls, filter_controls, rock_range_controls, wavelet_controls, explore_controls, pegleg
from theory.plotting import wiggle_plot
from theory.app.utils import mplfig_to_uri

plt.style.use('seaborn-dark')

layout = html.Div(
    [
        html.Div(
            [
                *component_controls,
                *wavelet_controls,
                explore_controls,
                *pipe_controls,
                rock_range_controls,
                *filter_controls,
                pegleg,
            ],
            className='d-flex flex-wrap'
        ),
        html.Div(
            [
                html.Div(html.Img(id="exploring-wavelets")),
            ],
            className="d-inline-flex flex-wrap",
        ),
    ]
)

@app.callback(
    dash.dependencies.Output("velocity-range-title", "children"),
    [
        Input("velocity-range-slider", "value"),
        Input("component-selector", "value"),
    ]
)
def update_alpha_range_title(value, component):
    if component == 'axial':
        return "alpha: {}".format('-'.join(str(v) for v in value))
    if component == 'tangential':
        return "beta: {}".format('-'.join(str(v) for v in value))

@app.callback(
    dash.dependencies.Output("gain-title", "children"),
    [dash.dependencies.Input("gain-slider", "value")],
)
def update_gain_title(value):
    return "gain: {}".format(str(value))

@app.callback(
    Output("exploring-wavelets", 'src'),
    [
        Input("wavelet-selector", "value"),
        Input("component-selector", "value"),
        Input("pipe-alpha-input", "value"),
        Input("pipe-rho-input", "value"),
        Input("pipe-beta-input", "value"),
        Input("pipe-rb-input", "value"),
        Input("bpf1", "value"),
        Input("bpf2", "value"),
        Input("bpf3", "value"),
        Input("bpf4", "value"),
        Input("rho-input-1", "value"),
        Input("velocity-range-slider", "value"),
        Input("velocity-step-input", "value"),
        Input("page-container", 'style'),
        Input("window-slider", 'value'),
        Input("gain-slider", 'value'),
        Input("pegleg-delay-input", 'value'),
        Input("pegleg-rc-input", 'value'),
        Input("pegleg-controls", 'value')
    ])
def update_figure(wavelet, component, pipe_alpha, pipe_rho, pipe_beta, pipe_rb,
                  bpf1, bpf2, bpf3, bpf4,
                  rho_1,# rho_2, rho_3,
                  velocity_range, velocity_step,
                  container_style, window, gain,
                  delay, rc, pegleg_controls
                  ):

    if 'add-pegleg' in pegleg_controls:
        add_pegleg = True
    else:
        add_pegleg = False

    rho_values = [rho_1]#, rho_2, rho_3]
    alpha_range = np.arange(velocity_range[0], velocity_range[1] + velocity_step, velocity_step)

    pipe = Pipe(Rb=pipe_rb, alpha=pipe_alpha, rho=pipe_rho, beta=pipe_beta,
                component=component)

    wavelets = []
    for a in alpha_range:
        rock = Rock(alpha=a, beta=a, rho=rho_values[-1], component=component)
        theoretical = TheoreticalWavelet(pipe, rock, component=component,
                                         filterby=[bpf1, bpf2, bpf3, bpf4])

        w = getattr(theoretical, '{}_in_time_domain'.format(wavelet))(
            window, filtered=True)
        if add_pegleg:
            w += theoretical.pegleg_effect(delay_in_ms=delay, RC=rc, window=window, filtered=True)
        wavelets.append(w)

    fig, ax = wiggle_plot(wavelets, alpha_range,
                          theoretical.get_time_range_for_window(window), gain=gain)
    ax.invert_yaxis()
    ax.grid()
    return mplfig_to_uri(fig)
