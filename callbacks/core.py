from dash import callback, Output, Input
from data.config import DATAFRAMES
from utils.compute_stats import filter_dataframes_by_labels
from utils.plot_utils.core import plot_core_aep_iteration_analysis

@callback(
    Output("aep-analysis-plot", "figure"),
    Input("mc-dropdown", "value")
)
def update_core_aep_iteration_analysis(selected_labels):
    """Callback zur Aktualisierung der iterationsspezifischen Metrikanalyse (Core-Tab)."""
    filtered_dfs = filter_dataframes_by_labels(DATAFRAMES, selected_labels)
    return plot_core_aep_iteration_analysis(filtered_dfs)