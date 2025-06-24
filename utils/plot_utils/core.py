import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from data.config import COLOR_MAP, METRIC_INFO
from utils.plot_utils.shared import apply_dark_mode_colors


def plot_aep_comparison(stats, dataframes):
    fig = make_subplots(
        rows=2, cols=3,
        specs=[
            [{"type": "bar"}, {"type": "bar"}, {"type": "box"}],
            [{"colspan": 2, "type": "scatter"}, None, {"type": "violin"}]
        ],
        subplot_titles=[
            "Mittelwert (GWh/yr)", "Unsicherheit (CV)", "Boxplots",
            "Jitterplot", "Violinplots"
        ],
        vertical_spacing=0.1,
        row_heights=[0.45, 0.55],
        column_widths=[0.25, 0.25, 0.5]
    )

    colors = [COLOR_MAP.get(label, "gray") for label in stats["labels"]]

    fig.add_trace(
        go.Bar(
            x=stats["labels"],
            y=stats["mean_aep"],
            marker_color=colors,
            text=[f"{v:.2f}" for v in stats["mean_aep"]],
            textfont=dict(color=colors),
            textposition="outside",
            showlegend=False
        ),
        row=1, col=1
    )

    fig.add_trace(
        go.Bar(
            x=stats["labels"],
            y=stats["aep_cv"],
            marker_color=colors,
            text=[f"{v:.2%}" for v in stats["aep_cv"]],
            textfont=dict(color=colors),
            textposition="outside",
            showlegend=False
        ),
        row=1, col=2
    )

    for label in stats["labels"]:
        fig.add_trace(
            go.Box(
                y=dataframes[label]["aep_final"],
                name=label,
                marker=dict(
                    color=COLOR_MAP.get(label, "grey"),
                    symbol="x",
                    size=6
                ),
                boxpoints="outliers",
                line=dict(width=0.5),
                marker_color=COLOR_MAP.get(label, "grey"),
                boxmean=True
            ),
            row=1, col=3
        )

    jittered_x = []
    jittered_y = []
    jittered_labels = []

    for i, label in enumerate(stats["labels"]):
        x_jitter = np.random.normal(loc=i, scale=0.1, size=len(dataframes[label]))
        jittered_x.extend(x_jitter)
        jittered_y.extend(dataframes[label]["aep_final"])
        jittered_labels.extend([label] * len(dataframes[label]))

    fig.add_trace(
        go.Scatter(
            x=jittered_x,
            y=jittered_y,
            mode="markers",
            showlegend=False,
            marker=dict(
                color=[COLOR_MAP.get(l, "gray") for l in jittered_labels],
                size=4,
                opacity=0.5
            )
        ),
        row=2, col=1
    )

    for label in stats["labels"]:
        fig.add_trace(
            go.Violin(
                y=dataframes[label]["aep_final"],
                name=label,
                line_color=COLOR_MAP.get(label, "gray"),
                box_visible=True,
                meanline_visible=True,
                showlegend=False
            ),
            row=2, col=3
        )

    fig.update_layout(
        height=750,
        showlegend=True,
        title=dict(
            text="Prognosebandbreite der AEP",
            x=0.5,
            font=dict(size=16)
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.1,
            xanchor="center",
            x=0.5,
            title=dict(text=None),
            font=dict(size=12)
        )
    )

    fig.update_xaxes(showline=True, linewidth=2, linecolor='gray', mirror=True)
    fig.update_yaxes(showline=True, linewidth=2, linecolor='gray', mirror=True)
    fig.update_yaxes(range=[0, max(stats["mean_aep"]) * 1.2], row=1, col=1)
    fig.update_yaxes(range=[0, max(stats["aep_cv"]) * 1.2], row=1, col=2)

    apply_dark_mode_colors(fig)

    for row in [1, 2]:
        for col in [1, 2, 3]:
            try:
                fig.update_xaxes(showticklabels=False, row=row, col=col)
            except Exception:
                pass

    return fig


def plot_core_aep_iteration_analysis(filtered_dfs, metric="aep_final"):
    fig = make_subplots(
        rows=2, cols=2,
        specs=[[{}, {}], [{"colspan": 2}, None]],
        vertical_spacing=0.1,
        row_heights=[0.5, 0.5]
    )

    for label, df in filtered_dfs.items():
        fig.add_trace(
            go.Histogram(
                x=df[metric],
                name=label,
                marker=dict(color=COLOR_MAP.get(label, "white")),
                opacity=0.6,
                nbinsx=100,
                showlegend=False
            ),
            row=1, col=1
        )

        fig.add_trace(
            go.Scatter(
                x=df["iav_nsim"],
                y=df[metric],
                name=label,
                mode="markers",
                showlegend=False,
                marker=dict(
                    color="rgba(0,0,0,0)",
                    size=6,
                    opacity=0.6,
                    line=dict(
                        color=COLOR_MAP.get(label, "white"),
                        width=1.5
                    )
                )
            ),
            row=1, col=2
        )

        fig.add_trace(
            go.Scatter(
                x=df["i"],
                y=df[metric],
                name=label,
                mode="lines",
                showlegend=False,
                line=dict(color=COLOR_MAP.get(label, "white"), width=0.5),
                opacity=0.2
            ),
            row=2, col=1
        )

        rolling = df[metric].rolling(window=50, center=True).mean()

        fig.add_trace(
            go.Scatter(
                x=df["i"],
                y=rolling,
                name=label,
                mode="lines",
                line=dict(color=COLOR_MAP.get(label, "white"), dash="dot", width=2),
                showlegend=True,
            ),
            row=2, col=1
        )

    fig.update_layout(
        height=750,
        title=dict(
            text="Iterationsspezifische Analyse der AEP",
            x=0.5,
            font=dict(size=16)
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5,
            title=None,
            font=dict(size=12)
        ),
        barmode="overlay",
        xaxis=dict(title=METRIC_INFO[metric]["metric_en"]),
        yaxis=dict(title="Frequency"),
        xaxis2=dict(title="IAV-Factor"),
        yaxis2=dict(title=METRIC_INFO[metric]["metric_en"]),
        xaxis3=dict(title="Iteration"),
        yaxis3=dict(title=METRIC_INFO[metric]["metric_en"]),
    )

    fig.update_xaxes(showline=True, linewidth=2, linecolor='gray', mirror=True)
    fig.update_yaxes(showline=True, linewidth=2, linecolor='gray', mirror=True)

    apply_dark_mode_colors(fig)

    return fig