from dash import callback, Output, Input
from data.config import LONGTERM_DFS
from utils.plot_utils.lt import (
    plot_lt_energy_evolution,
    plot_lt_energy_slope_comparison
)

@callback(
    Output("lt-evolution-plot", "figure"),
    Input("lt-mc-dropdown", "value"),
    Input("lt-metric-dropdown", "value")
)
def update_lt_energy_evolution_plot(selected_labels, selected_column):
    """Aktualisiert die LT-Metrikentwicklung (z. B. Energie/Wind) im Zeitverlauf."""
    return plot_lt_energy_evolution(LONGTERM_DFS, selected_labels, column=selected_column)


@callback(
    Output("lt-slope-plot", "figure"),
    Input("lt-years-dropdown", "value"),
    Input("lt-left-dropdown", "value"),
    Input("lt-right-dropdown", "value"),
)
def update_lt_energy_slope_comparison(selected_years, selected_left_label, selected_right_label):
    """Vergleicht den Einfluss der Steigung (und Wind) auf Energie für zwei ausgewählte Reanalyse-Produkte."""
    return plot_lt_energy_slope_comparison(
        LONGTERM_DFS[selected_left_label],
        LONGTERM_DFS[selected_right_label],
        selected_years,
        selected_left_label,
        selected_right_label
    )

