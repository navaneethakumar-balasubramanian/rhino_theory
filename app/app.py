import dash
import dash_core_components as dcc
import dash_html_components as html

import numpy as np

from theory import Pipe, Rock, TheoreticalWavelet

import plotly.plotly as py
import plotly.graph_objs as go
from plotly import tools

external_stylesheets = [
    "https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"
]

app = dash.Dash(external_stylesheets=external_stylesheets)

app.layout = html.Div(
    [
        html.Div([html.H1("Rhino in Theory")]),
        html.Div(
            [
                html.H3("Debugging Wavelets"),
                html.Div(
                    [
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
    ],
    className="container",
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
    dash.dependencies.Output("window-title", "children"),
    [dash.dependencies.Input("window-slider", "value")],
)
def update_window_title(value):
    return "window: {}".format(str(value))


@app.callback(
    dash.dependencies.Output("wavelets", "figure"),
    [
        dash.dependencies.Input("alpha-slider", "value"),
        dash.dependencies.Input("rho-slider", "value"),
        dash.dependencies.Input("window-slider", "value"),
    ],
)
def update_figure(alpha, rho, window):

    j = np.arange(10001) + 1
    f = (j - 1) * 0.5

    pipe = Pipe(Ro=0.1365, Ri=0.0687, Rb=0.16, alpha=4875, rho=7800)
    rock = Rock(alpha, rho)
    wavelet = TheoreticalWavelet(pipe, rock, frequencies=f)

    frequency_domain_primary = wavelet.amp_phase2complex(
        *wavelet.primary_in_frequency_domain
    )
    frequency_domain_reflected = wavelet.amp_phase2complex(
        *wavelet.reflected_in_frequency_domain
    )

    frequencies_trace = go.Scatter(y=f, mode="lines", marker=dict(color="black"))

    primary_real = go.Scatter(y=frequency_domain_primary.real, marker=dict(color="red"))
    primary_imag = go.Scatter(y=frequency_domain_primary.imag, marker=dict(color="red"))
    reflected_real = go.Scatter(
        y=frequency_domain_reflected.real, marker=dict(color="green")
    )
    reflected_imag = go.Scatter(
        y=frequency_domain_reflected.imag, marker=dict(color="green")
    )

    primary_nyquist = go.Scatter(
        x=frequency_domain_primary.real,
        y=frequency_domain_primary.imag,
        marker=dict(color="red"),
    )
    reflected_nyquist = go.Scatter(
        x=frequency_domain_reflected.real,
        y=frequency_domain_reflected.imag,
        marker=dict(color="green"),
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
        rows=7,
        cols=7,
        specs=[
            [None, {"colspan": 4, "rowspan": 2}, None, None, None, None, None],
            [None, None, None, None, None, None, None],
            [{"colspan": 3}, None, None, {"colspan": 3}, None, None, {"colspan": 1}],
            [{"colspan": 3}, None, None, {"colspan": 3}, None, None, {"colspan": 1}],
            [
                {"colspan": 2, "rowspan": 1},
                None,
                {"colspan": 2, "rowspan": 1},
                None,
                {"colspan": 2, "rowspan": 1},
                None,
                None,
            ],
            [
                {"colspan": 2, "rowspan": 2},
                None,
                {"colspan": 2, "rowspan": 2},
                None,
                {"colspan": 2, "rowspan": 2},
                None,
                None,
            ],
            [None, None, None, None, None, None, None],
        ],
        subplot_titles=(
            "Frequency Plot",
            "Primary - Real (freq)",
            "Primary - Imag (freq)",
            "Primary - Nyquist",
            "Reflected - Real (freq)",
            "Reflected - Imag (freq)",
            "Reflected - Nyquist",
            "Primary Wavelet (time)",
            "Reflected Wavelet (time)",
            "Multiple Wavelet",
        ),
    )

    fig.append_trace(frequencies_trace, 1, 2)
    fig.append_trace(primary_real, 3, 1)
    fig.append_trace(primary_imag, 3, 4)
    fig.append_trace(primary_nyquist, 3, 7)
    fig.append_trace(reflected_real, 4, 1)
    fig.append_trace(reflected_imag, 4, 4)
    fig.append_trace(reflected_nyquist, 4, 7)
    fig.append_trace(primary_wavelet_full, 5, 1)
    fig.append_trace(reflected_wavelet_full, 5, 3)
    fig.append_trace(multiple_wavelet_full, 5, 5)
    fig.append_trace(primary_wavelet, 6, 1)
    fig.append_trace(reflected_wavelet, 6, 3)
    fig.append_trace(multiple_wavelet, 6, 5)

    fig["layout"].update(height=1000, width=1000, showlegend=False, template="seaborn")

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
