from dash import callback, Output, Input
from data.config import DATAFRAMES, POR_SCATTERFRAMES, POR_DATAFRAMES, GROSS_POR_OBSERVED
from utils.plot_utils.por import (
    plot_por_energy_distribution,
    plot_por_regression_analysis,
    plot_por_energy_timeseries
)

@callback(
    Output("por-histogram-violin-plot", "figure"),
    Input("por-label-1-dropdown", "value"),
    Input("por-label-2-dropdown", "value"),
    Input("por-options", "value")
)
def update_por_energy_distribution_plot(label1, label2, options):
    """Verteilung der modellierten Jahresenergie (Histogramm & Violinplot, POR-Tab)."""
    df1 = DATAFRAMES[label1]
    df2 = DATAFRAMES[label2]
    return plot_por_energy_distribution(df1, df2, label1, label2, GROSS_POR_OBSERVED, options)


@callback(
    Output("reg-scatter", "figure"),
    Input("reg-scatter-label-dropdown-1", "value"),
    Input("reg-scatter-label-dropdown-2", "value"),
    Input("por-metric-dropdown", "value"),
    Input("por-metric-value-dropdown", "value"),
)
def update_por_regression_plot(label1, label2, reg_metric, metric_value):
    """Regressionsanalyse der besten Iteration (POR-Tab)."""
    df1 = POR_SCATTERFRAMES[label1]
    df2 = POR_SCATTERFRAMES[label2]
    return plot_por_regression_analysis(df1, df2, reg_metric, metric_value, label1, label2)


@callback(
    Output("timeseries-energy-plot", "figure"),
    Input("timeseries-labels-dropdown", "value"),
    Input("timeseries-metric-dropdown", "value"),
    Input("timeseries-metric-method-dropdown", "value")
)
def update_por_energy_timeseries_plot(selected_labels, metric, method):
    """Modellierte Zeitreihe der monatlichen Energie im POR-Zeitraum."""
    return plot_por_energy_timeseries(POR_DATAFRAMES, selected_labels, metric=metric, method=method)