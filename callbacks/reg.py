import pandas as pd

from dash import callback, Output, Input
from data.config import DATAFRAMES
from utils.plot_utils.reg import (
    plot_reg_model_distribution,
    plot_reg_model_metric_scatter,
    plot_reg_model_correlation_matrix
)

METRICS_FOR_CORRELATION = ["slope", "intercept", "mse", "r2", "iav", "aep", "aep_final"]

@callback(
    Output("model-comparison-plot", "figure"),
    Input("metric-dropdown", "value"),
    Input("label-1-dropdown", "value"),
    Input("label-2-dropdown", "value")
)
def update_reg_model_distribution(metric, label1, label2):
    """Vergleicht Modellmetriken mit Histogramm & Violinplot (Reg-Tab)."""
    df1 = DATAFRAMES[label1]
    df2 = DATAFRAMES[label2]
    return plot_reg_model_distribution(df1, df2, metric, label1, label2)


@callback(
    Output("modell-scatterplot", "figure"),
    Input("x-metric-dropdown", "value"),
    Input("y-metric-dropdown", "value"),
    Input("z-metric-dropdown", "value"),
    Input("size-metric-dropdown", "value"),
    Input("scatter-label-1-dropdown", "value"),
    Input("scatter-label-2-dropdown", "value"),
    Input("filter-metric-dropdown", "value"),
    Input("filter-range-slider", "value"),
)
def update_reg_model_metric_scatter(x_metric, y_metric, z_metric, size_metric,
                                    label1, label2, filter_metric, filter_range):
    df1 = DATAFRAMES[label1]
    df2 = DATAFRAMES[label2]

    df1_filtered = df1[
        (df1[filter_metric] >= filter_range[0]) &
        (df1[filter_metric] <= filter_range[1])
    ]
    df2_filtered = df2[
        (df2[filter_metric] >= filter_range[0]) &
        (df2[filter_metric] <= filter_range[1])
    ]

    return plot_reg_model_metric_scatter(
        df1_filtered, df2_filtered,
        x_metric, y_metric, z_metric, size_metric,
        label1, label2
    )


@callback(
    Output("filter-range-slider", "min"),
    Output("filter-range-slider", "max"),
    Output("filter-range-slider", "value"),
    Input("filter-metric-dropdown", "value"),
    Input("scatter-label-1-dropdown", "value"),
    Input("scatter-label-2-dropdown", "value")
)
def update_slider_bounds(metric, label1, label2):
    df1 = DATAFRAMES[label1]
    df2 = DATAFRAMES[label2]
    all_values = pd.concat([df1[metric], df2[metric]])
    min_val = float(all_values.min())
    max_val = float(all_values.max())
    return min_val, max_val, [min_val, max_val]


@callback(
    Output("correlation-matrix", "figure"),
    Input("corr-left-label-dropdown", "value"),
    Input("corr-right-label-dropdown", "value")
)
def update_reg_model_correlation_matrix(left_label, right_label):
    """Zeigt Korrelationen zwischen Modellmetriken für zwei Produkte (Reg-Tab)."""
    df_left = DATAFRAMES[left_label]
    df_right = DATAFRAMES[right_label]
    return plot_reg_model_correlation_matrix(df_left, df_right, left_label, right_label, METRICS_FOR_CORRELATION)