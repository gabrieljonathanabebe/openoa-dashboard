import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from data.config import COLOR_MAP
from utils.plot_utils.shared import (
    apply_dark_mode_colors,
    get_global_axis_range,
    get_global_color_scale_bounds
)

from utils.compute_stats import compute_lt_metrics, filter_lt_data


def plot_lt_energy_evolution(dataframes, selected_labels, column="energy"):
    title_left = "LT-Bruttoenergie" if column == "energy" else "LT-Wind"
    title_right = "IAV-Energie" if column == "energy" else "IAV-Wind"

    fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=[title_left, title_right],
        shared_xaxes=False
    )

    for label in selected_labels:
        df = dataframes[label]
        years, non_cum_mean, cum_mean, cum_cv = compute_lt_metrics(df, column=column)

        fig.add_trace(
            go.Scatter(
                x=years,
                y=cum_mean,
                mode="lines",
                name=label,
                hovertemplate="Jahr: %{x}<br>Energie (kumuliert): %{y:.2f} GWh/yr",
                line=dict(color=COLOR_MAP.get(label, "gray"))
            ),
            row=1, col=1
        )

        fig.add_trace(
            go.Scatter(
                x=years,
                y=non_cum_mean,
                mode="lines",
                name=label,
                hovertemplate="Jahr: %{x}<br>Energie: %{y:.2f} GWh/yr",
                opacity=0.5,
                line=dict(color=COLOR_MAP.get(label, "gray"), dash="dot"),
                showlegend=False
            ),
            row=1, col=1
        )

        fig.add_trace(
            go.Scatter(
                x=years,
                y=cum_cv,
                mode="lines",
                name=label,
                hovertemplate="Jahr: %{x}<br>IAV: %{y:.2f} %",
                line=dict(color=COLOR_MAP.get(label, "gray"))
            ),
            row=1, col=2
        )

    fig.update_layout(
        height=500,
        title=dict(
            text="LT-Entwicklung",
            x=0.5,
            font=dict(size=16)
        ),
        showlegend=False,
        xaxis=dict(title="Jahr"),
        yaxis=dict(title="LT-Energy (GWh/yr)" if column == "energy" else "Average LT-Windspeed (m/s)"),
        xaxis2=dict(title="Jahr"),
        yaxis2=dict(title="IAV-Energy (%)" if column == "energy" else "IAV-Wind (%)")
    )

    fig.update_xaxes(showline=True, linewidth=2, linecolor='gray', mirror=True)
    fig.update_yaxes(showline=True, linewidth=2, linecolor='gray', mirror=True)

    apply_dark_mode_colors(fig)

    return fig


def plot_lt_energy_slope_comparison(left_df, right_df, selected_years, left_label, right_label):
    left_filtered = filter_lt_data(left_df, selected_years)
    right_filtered = filter_lt_data(right_df, selected_years)

    x_min, x_max = get_global_axis_range("slope", left_filtered, right_filtered)
    color_min, color_max = get_global_color_scale_bounds("wind", left_filtered, right_filtered)

    fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=[left_label, right_label],
        shared_xaxes=True,
        shared_yaxes=True
    )

    fig.add_trace(
        go.Scatter(
            x=left_filtered["slope"],
            y=left_filtered["energy"],
            mode="markers",
            marker=dict(
                color=left_filtered["wind"],
                colorscale="RdBu",
                cmin=color_min,
                cmax=color_max,
                colorbar=dict(
                    title=dict(text="Average LT-Windspeed (m/s)", side="right")
                ),
                showscale=True,
                size=5,
                line=dict(color="rgba(255,255,255,0.4)", width=0.2)
            ),
            name=left_label,
            customdata=np.stack((left_filtered["year"],), axis=-1),
            hovertemplate=(
                "Jahr: %{customdata[0]}<br>"
                "Steigung: %{x:.3f} GWh/(m/s)<br>"
                "Energie: %{y:.2f} GWh/yr<br>"
                "Wind: %{marker.color:.2f} m/s<br><extra></extra>"
            ),
            showlegend=False
        ),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(
            x=right_filtered["slope"],
            y=right_filtered["energy"],
            mode="markers",
            marker=dict(
                color=right_filtered["wind"],
                colorscale="RdBu",
                showscale=False,
                size=5,
                line=dict(color="rgba(255,255,255,0.5)", width=0.2)
            ),
            name=right_label,
            customdata=np.stack((right_filtered["year"],), axis=-1),
            hovertemplate=(
                "Jahr: %{customdata[0]}<br>"
                "Steigung: %{x:.3f} GWh/(m/s)<br>"
                "Energie: %{y:.2f} GWh/yr<br>"
                "Wind: %{marker.color:.2f} m/s<br><extra></extra>"
            ),
            showlegend=False
        ),
        row=1, col=2
    )

    fig.update_layout(
        height=500,
        title=dict(
            text="Einfluss der Steigung auf die LT-Energie in Abhängigkeit der Windressourcen",
            x=0.5,
            font=dict(size=16)
        ),
        showlegend=False,
        xaxis=dict(title="Slope (GWh/ (m/s))", range=[x_min, x_max]),
        yaxis=dict(title="LT-Energy (GWh/yr)"),
        xaxis2=dict(title="Slope (GWh/ (m/s))", range=[x_min, x_max]),
        yaxis2=dict(title="LT-Energy (GWh/yr)")
    )

    fig.update_xaxes(showline=True, linewidth=2, linecolor='gray', mirror=True)
    fig.update_yaxes(showline=True, linewidth=2, linecolor='gray', mirror=True)

    apply_dark_mode_colors(fig)

    return fig