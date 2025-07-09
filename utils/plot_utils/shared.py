import pandas as pd

def apply_dark_mode_colors(fig):
    layout_updates = {
        "plot_bgcolor": "#2c2c2c",
        "paper_bgcolor": "#2c2c2c",
        "font": dict(family="Roboto", color="white"),
        "legend": dict(font=dict(color="white")),
    }

    # Alle x- und y-Achsen anpassen
    for i in range(1, 10):  # falls mehr Subplots folgen
        layout_updates[f"xaxis{i}"] = dict(color="white", gridcolor="#444444")
        layout_updates[f"yaxis{i}"] = dict(color="white", gridcolor="#444444")

    # Fallback für einfache Layouts (z. B. fig = go.Figure())
    layout_updates["xaxis"] = dict(color="white", gridcolor="#444444")
    layout_updates["yaxis"] = dict(color="white", gridcolor="#444444")

    fig.update_layout(**layout_updates)
    return fig


def normalize_bubble_size(series, min_size=3, max_size=20, global_min=None, global_max=None):
    global_min = series.min() if global_min is None else global_min
    global_max = series.max() if global_max is None else global_max
    norm = (series - global_min) / (global_max - global_min + 1e-9)
    return norm * (max_size - min_size) + min_size



def get_global_axis_range(column, *dfs, padding_factor=0.05):
    all_values = pd.concat([df[column] for df in dfs])
    min_val = all_values.min()
    max_val = all_values.max()

    range_span = max_val - min_val
    padding = range_span * padding_factor

    return min_val - padding, max_val + padding


def get_global_color_scale_bounds(column, *dfs):
    all_values = pd.concat([df[column] for df in dfs])
    return all_values.min(), all_values.max()

def get_global_size_bounds(column, *dfs):
    all_values = pd.concat([df[column] for df in dfs])
    return all_values.min(), all_values.max()


def break_label(text, threshold=10):
    if len(text) > threshold:
        return text.replace(" ", "<br>", 1)  # Nur erstes Leerzeichen umbrechen
    return text