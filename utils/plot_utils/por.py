import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from utils.plot_utils.shared import apply_dark_mode_colors, get_global_axis_range
from data.config import COLOR_MAP, METRIC_INFO
from utils.compute_stats import get_iteration



def plot_por_energy_distribution(df1, df2, label1, label2, observed_value, options):
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=["Histogramm", "Split-Violinplot"],
        specs=[[{"type": "histogram"}, {"type": "violin"}]],
        column_widths=[0.5, 0.5]
    )

    for df, label, color, side in zip(
        [df1, df2],
        [label1, label2],
        [COLOR_MAP.get(label1, "gray"), COLOR_MAP.get(label2, "gray")],
        ["negative", "positive"]
    ):
        gps_vals = df["gps"]
        mean_val = np.mean(gps_vals)
        label_with_mean = f"{label} (μ={mean_val:.2f})"

        fig.add_trace(
            go.Histogram(
                x=gps_vals,
                name=label,
                marker_color=color,
                opacity=0.6,
                showlegend=False
            ),
            row=1, col=1
        )

        if "show-means" in options:
            fig.add_vline(
                x=mean_val,
                line=dict(color=color, dash="dash"),
                row=1, col=1
            )

        fig.add_trace(
            go.Violin(
                y=gps_vals,
                x=["Vergleich"] * len(gps_vals),
                side=side,
                name=label_with_mean,
                line_color=color,
                fillcolor=color,
                opacity=0.7,
                points="all",
                meanline_visible=True,
                showlegend=True
            ),
            row=1, col=2
        )

        if "show-means" in options:
            fig.add_hline(
                y=mean_val,
                line=dict(color=color, dash="dash"),
                row=1, col=2
            )

        if "show-observed" in options:
            fig.add_vline(
                x=observed_value,
                line=dict(color="white", dash="dash"),
                annotation_text=f"μ Beobachtet: {observed_value:.2f}",
                annotation_position="top left",
                annotation=dict(font=dict(color="white")),
                row=1, col=1
            )
            fig.add_hline(
                y=observed_value,
                line=dict(color="white", dash="dash"),
                annotation_text=f"μ Beobachtet: {observed_value:.2f}",
                annotation_position="top right",
                annotation=dict(font=dict(color="white")),
                row=1, col=2
            )

    fig.update_layout(
        height=500,
        title=dict(
            text="Verteilung der modellierten Jahresenergie (GPS)",
            x=0.5,
            font=dict(size=16)
        ),
        barmode="overlay",
        violinmode="overlay",
        xaxis=dict(title=METRIC_INFO["gps"]["metric_en"]),
        yaxis=dict(title="Frequency"),
        yaxis2=dict(title=METRIC_INFO["gps"]["metric_en"]),
        legend=dict(orientation="h", y=-0.2, x=0.5, xanchor="center")
    )

    fig.update_xaxes(showline=True, linewidth=2, linecolor='gray', mirror=True)
    fig.update_yaxes(showline=True, linewidth=2, linecolor='gray', mirror=True)

    apply_dark_mode_colors(fig)
    return fig


def plot_por_regression_analysis(df1, df2, metric, value, label1, label2):
    def add_trace(fig, df, source, color, symbol, name, row=1, col=1, showlegend=True):
        filtered = df[df["source"] == source]
        fig.add_trace(
            go.Scatter(
                x=filtered["wind_speed"],
                y=filtered["energy"],
                mode="markers",
                marker=dict(color=color, symbol=symbol, size=7),
                name=name,
                showlegend=showlegend
            ),
            row=row, col=col
        )

    iter1 = get_iteration(df1, metric, method=value)
    iter2 = get_iteration(df2, metric, method=value)
    df1_filtered = df1[df1["iteration"] == iter1]
    df2_filtered = df2[df2["iteration"] == iter2]

    x_min, x_max = get_global_axis_range("wind_speed", df1_filtered, df2_filtered)
    y_min, y_max = get_global_axis_range("energy", df1_filtered, df2_filtered)

    fig = make_subplots(rows=1, cols=2, subplot_titles=[label1, label2], horizontal_spacing=0.05)

    add_trace(fig, df1_filtered, "bootstrap", "green", "circle", "Bootstrap", col=1, showlegend=True)
    add_trace(fig, df1_filtered, "non-bootstrap", "red", "x", "Non-Bootstrap", col=1, showlegend=True)

    slope1 = df1_filtered["slope"].iloc[0]
    intercept1 = df1_filtered["intercept"].iloc[0]
    x_vals1 = np.linspace(x_min, x_max, 100)
    y_vals1 = slope1 * x_vals1 + intercept1

    fig.add_trace(
        go.Scatter(
            x=x_vals1,
            y=y_vals1,
            mode="lines",
            line=dict(color="green", dash="dash"),
            name="",
            showlegend=False
        ),
        row=1, col=1
    )

    add_trace(fig, df2_filtered, "bootstrap", "green", "circle", "Bootstrap", col=2, showlegend=False)
    add_trace(fig, df2_filtered, "non-bootstrap", "red", "x", "Non-Bootstrap", col=2, showlegend=False)

    slope2 = df2_filtered["slope"].iloc[0]
    intercept2 = df2_filtered["intercept"].iloc[0]
    x_vals2 = np.linspace(x_min, x_max, 100)
    y_vals2 = slope2 * x_vals2 + intercept2

    fig.add_trace(
        go.Scatter(
            x=x_vals2,
            y=y_vals2,
            mode="lines",
            line=dict(color="green", dash="dash"),
            name="",
            showlegend=False
        ),
        row=1, col=2
    )

    fig.add_annotation(
        text=f"y = {slope1:.3f}x + {intercept1:.2f}<br>R² = {df1_filtered['r2'].iloc[0]:.2f}<br>"
             f"MSE = {df1_filtered['mse'].iloc[0]:.3f}<br>"
             f"Bias = {df1_filtered['yearly_bias'].iloc[0]:.3f}",
        xref="paper", yref="paper",
        x=0.02, y=0.95,
        showarrow=False,
        font=dict(color="white", size=12)
    )

    fig.add_annotation(
        text=f"y = {slope2:.3f}x + {intercept2:.2f}<br>R² = {df2_filtered['r2'].iloc[0]:.2f}<br>"
             f"MSE = {df2_filtered['mse'].iloc[0]:.3f}<br>"
             f"Bias = {df2_filtered['yearly_bias'].iloc[0]:.3f}",
        xref="paper", yref="paper",
        x=0.60, y=0.95,
        showarrow=False,
        font=dict(color="white", size=12)
    )

    fig.update_layout(
        height=450,
        title=dict(
            text="Regressionplots einer ausgewählten Iteration",
            x=0.5,
            font=dict(size=16)
        ),
        xaxis=dict(title="POR-Windspeed (m/s)"),
        yaxis=dict(title="POR-Gross-Energy (GWh/m)"),
        xaxis2=dict(title="POR-Windspeed (m/s)"),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        )
    )

    fig.update_xaxes(showline=True, linewidth=2, linecolor='gray', mirror=True, range=[x_min, x_max])
    fig.update_yaxes(showline=True, linewidth=2, linecolor='gray', mirror=True, range=[y_min, y_max])

    apply_dark_mode_colors(fig)
    return fig


def plot_por_energy_timeseries(df_dict, selected_labels, metric="r2", method="max"):
    fig = go.Figure()

    for label in selected_labels:
        df_label = df_dict[label]
        best_iter = get_iteration(df_label, metric, method)
        df_iter = df_label[df_label["iteration"] == best_iter].copy().sort_values("time")

        fig.add_trace(go.Scatter(
            x=df_iter["time"],
            y=df_iter["pred_energy"],
            mode="lines+markers",
            name=f"{label} (modelliert)",
            line=dict(color=COLOR_MAP.get(label, "gray"), width=2),
            marker=dict(size=6)
        ))

    any_df = list(df_dict.values())[0]
    ref = (
        any_df.groupby("time", as_index=False)["gross_energy_gwh"]
        .first()
        .sort_values("time")
    )

    fig.add_trace(go.Scatter(
        x=ref["time"],
        y=ref["gross_energy_gwh"],
        mode="lines+markers",
        name="Beobachtete Energie (Referenz)",
        line=dict(color="white", width=2, dash="dot"),
        marker=dict(size=6)
    ))

    fig.update_layout(
        title=dict(
            text="Zeitreihe der modellierten monatlichen Energie im POR-Zeitraum",
            x=0.5,
            font=dict(size=16)
        ),
        height=450,
        xaxis=dict(
            title="Monat",
            rangeslider=dict(visible=True),
            type="date"
        ),
        yaxis_title="Energie (GWh)",
        legend=dict(orientation="h", y=-0.8, x=0.5, xanchor="center")
    )

    fig.update_xaxes(showline=True, linewidth=2, linecolor='gray', mirror=True)
    fig.update_yaxes(showline=True, linewidth=2, linecolor='gray', mirror=True)

    apply_dark_mode_colors(fig)
    return fig