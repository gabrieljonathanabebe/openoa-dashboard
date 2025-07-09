import plotly.graph_objects as go
from plotly.subplots import make_subplots

from data.config import COLOR_MAP, METRIC_INFO
from utils.plot_utils.shared import (
    apply_dark_mode_colors,
    get_global_axis_range,
    get_global_color_scale_bounds,
    get_global_size_bounds,
    break_label,
    normalize_bubble_size
)



def plot_reg_model_distribution(df1, df2, metric, label1, label2):
    fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=["Histogramm", "Split-Violinplot"],
        specs=[[{"type": "histogram"}, {"type": "violin"}]],
        column_widths=[0.5, 0.5],
    )

    for df, label, color, side in zip(
        [df1, df2],
        [label1, label2],
        [COLOR_MAP.get(label1, "gray"), COLOR_MAP.get(label2, "gray")],
        ["negative", "positive"]
    ):
        fig.add_trace(
            go.Histogram(
                x=df[metric],
                name=label,
                opacity=0.6,
                marker_color=color,
                showlegend=False
            ),
            row=1, col=1
        )
        fig.add_trace(
            go.Violin(
                y=df[metric],
                x=["Vergleich"] * len(df),
                side=side,
                name=label,
                line_color=color,
                fillcolor=color,
                opacity=0.7,
                meanline_visible=True,
                showlegend=True,
                points="all"
            ),
            row=1, col=2
        )

    fig.update_layout(
        height=500,
        barmode="overlay",
        violinmode="overlay",
        title=dict(
            text=f"Verteilung der Modellgüte: {METRIC_INFO[metric]['metric_en']}",
            x=0.5,
            font=dict(size=16)
        ),
        legend=dict(orientation="h", y=-0.2, x=0.5, xanchor="center"),
        xaxis=dict(title=METRIC_INFO[metric]["metric_en"]),
        yaxis=dict(title="Frequency"),
        yaxis2=dict(title=METRIC_INFO[metric]["metric_en"]),
    )

    fig.update_xaxes(showline=True, linewidth=2, linecolor='gray', mirror=True)
    fig.update_yaxes(showline=True, linewidth=2, linecolor='gray', mirror=True)

    apply_dark_mode_colors(fig)
    return fig


def plot_reg_model_metric_scatter(df1, df2, x_metric, y_metric, z_metric, size_metric, label1, label2):
    x_min, x_max = get_global_axis_range(x_metric, df1, df2)
    y_min, y_max = get_global_axis_range(y_metric, df1, df2)
    cmin, cmax = get_global_color_scale_bounds(z_metric, df1, df2)
    size_min, size_max = get_global_size_bounds(size_metric, df1, df2)

    fig = make_subplots(
        rows=1,
        cols=2,
        column_titles=[label1, label2],
        column_widths=[0.5, 0.5],
        shared_xaxes=True,
        shared_yaxes=True,
    )

    for df, label, col in zip(
        [df1, df2], [label1, label2], [1, 2]
    ):
        show_colorbar = (label == label2)
        fig.add_trace(
            go.Scatter(
                x=df[x_metric],
                y=df[y_metric],
                mode="markers",
                name=label,
                showlegend=False,
                marker=dict(
                    size=normalize_bubble_size(df[size_metric], min_size=3, max_size=20, global_min=size_min, global_max=size_max),
                    color=df[z_metric],
                    colorscale="viridis",
                    cmin=cmin,
                    cmax=cmax,
                    showscale=show_colorbar,
                    colorbar=dict(
                        title=dict(
                            text=METRIC_INFO[z_metric]['metric_en'],
                            side="right"
                        )
                    ) if show_colorbar else None,
                    opacity=0.7,
                    line=dict(
                        color="gray",       
                        width=0.5          
                    )
                )
            ),
            row=1, col=col
        )

    fig.update_layout(
        height=450,
        title=dict(
            text=(
                f"Zusammenhang zwischen "
                f"{METRIC_INFO[x_metric]['metric_en']}, "
                f"{METRIC_INFO[y_metric]['metric_en']} und "
                f"{METRIC_INFO[z_metric]['metric_en']}"
            ),
            x=0.5,
            font=dict(size=16)
        ),
        xaxis=dict(title=METRIC_INFO[x_metric]["metric_en"], range=[x_min, x_max]),
        xaxis2=dict(title=METRIC_INFO[x_metric]["metric_en"], range=[x_min, x_max]),
        yaxis=dict(title=METRIC_INFO[y_metric]["metric_en"], range=[y_min, y_max]),
        yaxis2=dict(title=METRIC_INFO[y_metric]["metric_en"], range=[y_min, y_max]),
    )

    fig.update_xaxes(showline=True, linewidth=2, linecolor='gray', mirror=True)
    fig.update_yaxes(showline=True, linewidth=2, linecolor='gray', mirror=True)

    apply_dark_mode_colors(fig)
    return fig


def plot_reg_model_correlation_matrix(left_df, right_df, title_left, title_right, metrics):
    def compute_corr(df):
        return df[metrics].corr()

    corr_left = compute_corr(left_df)
    corr_right = compute_corr(right_df)

    x_labels = [break_label(METRIC_INFO[m]["metric_en"]) for m in metrics]
    y_labels = [break_label(METRIC_INFO[m]["metric_en"]) for m in metrics]

    fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=[title_left, title_right],
        horizontal_spacing=0.05
    )

    heatmap_kwargs = dict(
        zmin=-1,
        zmax=1,
        colorscale=[(0, "red"), (0.5, "white"), (1, "green")],
        colorbar=dict(title="Korrelation")
    )

    fig.add_trace(
        go.Heatmap(
            z=corr_left.values,
            x=x_labels,
            y=y_labels,
            text=[[f"{val:.2f}" for val in row] for row in corr_left.values],
            texttemplate="%{text}",
            **heatmap_kwargs
        ),
        row=1, col=1
    )

    fig.add_trace(
        go.Heatmap(
            z=corr_right.values,
            x=x_labels,
            y=y_labels,
            text=[[f"{val:.2f}" for val in row] for row in corr_right.values],
            texttemplate="%{text}",
            showscale=False,
            **heatmap_kwargs
        ),
        row=1, col=2
    )

    fig.update_layout(
        height=500,
        title="Korrelationen zwischen Modellkoeffizienten",
        title_x=0.5,
    )

    fig.update_yaxes(showticklabels=False, row=1, col=2)

    apply_dark_mode_colors(fig)
    return fig