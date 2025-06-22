import dash
from dash import dcc, html, Output, Input, callback_context, ALL

import datetime
import os

from layout.tab01_home import tab_home_layout
from layout.tab02_data import tab_data_layout
from layout.tab03_core import tab_core_layout
from layout.tab04_lt import tab_lt_layout
from layout.tab05_sensitivity import tab_sensitivity_layout
from layout.tab06_por import tab_por_layout
from layout.tab07_glossary import tab_glossary_layout

from utils.compute_stats import filter_dataframes_by_labels

from utils.plot_utils import (
    get_aep_analysis_plot,
    get_lt_evolution_plot,
    get_slope_energy_plot,
    get_model_comparison_plot,
    get_model_scatter_plot,
    get_por_hist_violin_plot,
    get_correlation_matrices,
    get_regression_plot,
    get_por_timeseries_plot
)

from data.config import (
    DATAFRAMES, 
    LONGTERM_DFS, 
    TAB_KEYWORDS,
    WEEKDAY_MAP,
    MONTH_MAP,
    GROSS_POR_OBSERVED,
    POR_SCATTERFRAMES,
    POR_DATAFRAMES
)



external_stylesheets = [
    "/assets/styles.css",
    "https://use.fontawesome.com/releases/v5.15.4/css/all.css"  # ältere, sehr stabile Version
]
                         
app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=external_stylesheets
)


app.layout = html.Div([
    dcc.Location(id="url"),

    # --- Sticky Header ---
    html.Div([
        html.Div([
            html.I(className="fas fa-chart-bar", style={"marginRight": "8px"}),
            "Windpark-Dashboard"
        ], style={
            "fontWeight": "bold",
            "fontSize": "20px",
            "color": "#EAEAEA",
            "display": "flex",
            "alignItems": "center"
        }),

        html.Div([
            html.Div([
                dcc.Input(
                    id="search-input",
                    placeholder="Suchen...",
                    style={
                        "padding": "10px",
                        "width": "300px",
                        "fontSize": "16px",
                        "borderRadius": "8px",
                        "backgroundColor": "#1f1f1f",
                        "color": "#EAEAEA",
                        "border": "1px solid #444"
                    }
                ),
                html.Ul(id="search-suggestions", className="search-suggestions")
            ], style={"position": "relative", "marginRight": "10px"}),

            html.I(className="fas fa-search", style={
                "fontSize": "20px",
                "color": "#EAEAEA",
                "marginRight": "15px"
            }),

            html.I(className="fas fa-cog", style={
                "fontSize": "20px",
                "color": "#EAEAEA",
                "marginRight": "15px",
                "cursor": "pointer"
            }),

            html.Div(id="current-time", className="current-time", style={
                "fontSize": "16px",
                "color": "#AAA",
                "minWidth": "110px"
            })
        ], style={"display": "flex", "alignItems": "center"})
    ], className="sticky-header", style={
        "display": "flex",
        "justifyContent": "space-between",
        "alignItems": "center",
        "padding": "10px 20px",
        "backgroundColor": "#2c2c2c",
        "borderBottom": "1px solid #444"
    }),

    # --- Content Wrapper: Sidebar + Main Content ---
    html.Div([
        # --- Sidebar ---
        html.Div([
            html.Div([
                html.I(className="fas fa-compass", style={"marginRight": "8px"}),
                html.Span("Navigation")
            ], className="sidebar-header"),

            html.Div([
                html.I(className="fas fa-home", style={"marginRight": "8px"}),
                html.Span("Allgemein")
            ], className="sidebar-category"),
            dcc.Link("Projekt", href="/", id="link-home", className="sidebar-link"),

            html.Div([
                html.I(className="fas fa-database", style={"marginRight": "8px"}),
                html.Span("Datenquellen")
            ], className="sidebar-category"),
            dcc.Link("Reanalyse & Energie", href="/data", id="link-data", className="sidebar-link"),

            html.Div([
                html.I(className="fas fa-chart-line", style={"marginRight": "8px"}),
                html.Span("Ergebnisse")
            ], className="sidebar-category"),
            dcc.Link("Zentrale Ergebnisse", href="/core", id="link-core", className="sidebar-link"),
            dcc.Link("Langzeitanalyse", href="/lt", id="link-lt", className="sidebar-link"),
            dcc.Link("Modellgüte", href="/sensitivity", id="link-sensitivity", className="sidebar-link"),
            dcc.Link("POR", href="/por", id="link-por", className="sidebar-link"),

            html.Div([
                html.I(className="fas fa-book", style={"marginRight": "8px"}),
                html.Span("Glossar")
            ], className="sidebar-category"),
            dcc.Link("Begriffe", href="/glossary", id="link-glossary", className="sidebar-link"),
            
            html.Div([
                html.A(
                    html.I(className="fab fa-github"), 
                    href="https://github.com/gabrieljonathanabebe", 
                    target="_blank", 
                    className="social-icon"
                ),
                html.A(
                    html.I(className="fab fa-linkedin"), 
                    href="https://www.linkedin.com/in/gabriel-jonathan-abebe-781b92316/", 
                    target="_blank", 
                    className="social-icon"
                ),
                html.A(
                    html.I(className="fas fa-envelope"), 
                    href="mailto:jonathanabebe@outlook.de", 
                    className="social-icon"
                ),
            ], className="sidebar-social")
        ], className="sidebar"),

        # --- Main Content Area ---
        html.Div(id="page-content", className="main-content")
    ], className="layout-container")
])
        


@app.callback(
    Output("page-content", "children"), 
    Input("url", "pathname")
)
def display_page(pathname):
    if pathname == "/data":
        return tab_data_layout
    elif pathname == "/core":
        return tab_core_layout
    elif pathname == "/lt":
        return tab_lt_layout
    elif pathname == "/sensitivity":
        return tab_sensitivity_layout
    elif pathname == "/por":
        return tab_por_layout
    elif pathname == "/glossary":
        return tab_glossary_layout
    else:
        return tab_home_layout  # Startseite
    

@app.callback(
    Output("link-home", "className"),
    Output("link-data", "className"),
    Output("link-core", "className"),
    Output("link-lt", "className"),
    Output("link-sensitivity", "className"),
    Output("link-por", "className"),
    Output("link-glossary", "className"),
    Input("url", "pathname")
)
def highlight_active_link(pathname):
    def get_class(link_path):
        return "sidebar-link selected" if pathname == link_path else "sidebar-link"

    return (
        get_class("/"),
        get_class("/data"),
        get_class("/core"),
        get_class("/lt"),
        get_class("/sensitivity"),
        get_class("/por"),
        get_class("/glossary")
    )
    

@app.callback(
    Output("aep-analysis-plot", "figure"),
    Input("mc-dropdown", "value"),
)
def update_aep_analysis_plot(selected_labels):
    filtered_dfs = filter_dataframes_by_labels(DATAFRAMES, selected_labels)
    return get_aep_analysis_plot(filtered_dfs)


@app.callback(
    Output("lt-evolution-plot", "figure"),
    Input("lt-mc-dropdown", "value"),
    Input("lt-metric-dropdown", "value")
)
def update_lt_evolution_plot(selected_labels, selected_column):
    return get_lt_evolution_plot(LONGTERM_DFS, selected_labels, column=selected_column)


@app.callback(
    Output("lt-slope-plot", "figure"),
    Input("lt-years-dropdown", "value"),
    Input("lt-left-dropdown", "value"),
    Input("lt-right-dropdown", "value"),
)
def update_slope_energy_plot(selected_years, selected_left_label, selected_right_label):
    return get_slope_energy_plot(
        LONGTERM_DFS[selected_left_label],
        LONGTERM_DFS[selected_right_label], 
        selected_years,
        selected_left_label,
        selected_right_label)

@app.callback(
    Output("model-comparison-plot", "figure"),
    Input("metric-dropdown", "value"),
    Input("label-1-dropdown", "value"),
    Input("label-2-dropdown", "value")
)
def update_model_comparison(metric, label1, label2):
    df1 = DATAFRAMES[label1]
    df2 = DATAFRAMES[label2]
    return get_model_comparison_plot(df1, df2, metric, label1, label2)


@app.callback(
    Output("modell-scatterplot", "figure"),
    Input("x-metric-dropdown", "value"),
    Input("y-metric-dropdown", "value"),
    Input("z-metric-dropdown", "value"),
    Input("scatter-label-1-dropdown", "value"),
    Input("scatter-label-2-dropdown", "value")
)
def update_model_scatter_plot(x_metric, y_metric, z_metric, label1, label2):
    df1 = DATAFRAMES[label1]
    df2 = DATAFRAMES[label2]
    return get_model_scatter_plot(df1, df2, x_metric, y_metric, z_metric, label1, label2)


@app.callback(
    Output("por-histogram-violin-plot", "figure"),
    Input("por-label-1-dropdown", "value"),
    Input("por-label-2-dropdown", "value"),
    Input("por-options", "value")
)
def update_por_plot(label1, label2, options):
    df1 = DATAFRAMES[label1]
    df2 = DATAFRAMES[label2]
    return get_por_hist_violin_plot(df1, df2, label1, label2, GROSS_POR_OBSERVED, options)
    

app.layout.children.append(
    dcc.Interval(id="clock-interval", interval=1000, n_intervals=0)  # jede Minute
)


METRICS_FOR_CORRELATION = ["slope", "intercept", "mse", "r2", "iav", "aep", "aep_final"]

@app.callback(
    Output("correlation-matrix", "figure"),
    Input("corr-left-label-dropdown", "value"),
    Input("corr-right-label-dropdown", "value")
)
def update_correlation_matrix(left_label, right_label):
    df_left = DATAFRAMES[left_label]
    df_right = DATAFRAMES[right_label]
    
    fig = get_correlation_matrices(df_left, df_right, left_label, right_label, METRICS_FOR_CORRELATION)
    return fig



@app.callback(
    Output("reg-scatter", "figure"),
    Input("reg-scatter-label-dropdown-1", "value"),
    Input("reg-scatter-label-dropdown-2", "value"),
    Input("por-metric-dropdown", "value"),
    Input("por-metric-value-dropdown", "value"),
)
def update_regression_plot(label1, label2, reg_metric, metric_value):
    df1 = POR_SCATTERFRAMES[label1]
    df2 = POR_SCATTERFRAMES[label2]

    fig = get_regression_plot(df1, df2, reg_metric, metric_value, label1, label2)
    return fig


@app.callback(
    Output("timeseries-energy-plot", "figure"),
    Input("timeseries-labels-dropdown", "value"),
    Input("timeseries-metric-dropdown", "value"),
    Input("timeseries-metric-method-dropdown", "value")
)
def update_por_timeseries(selected_labels, metric, method):
    return get_por_timeseries_plot(POR_DATAFRAMES, selected_labels, metric=metric, method=method)


@app.callback(
    Output("current-time", "children"),
    Input("clock-interval", "n_intervals")
)
def update_clock(n):
    now = datetime.datetime.now()
    weekday = now.strftime("%a")  # z. B. "Wed"
    day = now.day
    month = now.strftime("%B")    # z. B. "June"
    time = now.strftime("%H:%M:%S")

    # Wörterbuch verwenden
    weekday_de = WEEKDAY_MAP.get(weekday, weekday)
    month_de = MONTH_MAP.get(month, month)

    return f"{weekday_de} {day}. {month_de} {time}"


@app.callback(
    Output("search-suggestions", "children"),
    Input("search-input", "value"),
    prevent_initial_call = True
)
def update_search_suggestions(query):
    if not query:
        return []
    
    query = query.lower()
    suggestions = []
    
    for tab_id, keywords in TAB_KEYWORDS.items():
        score = sum(1 for kw in keywords if query in kw.lower())
        if score > 0:
            suggestions.append((score, tab_id))
            
    suggestions.sort(reverse=True)
    
    tab_labels = {
    "tab-home": "🏠 Projekt",
    "tab-data": "🌍 Energiedaten",
    "tab-core": "📈 Zentrale Ergebnisse",
    "tab-lt": "📉 Langzeitanalyse",
    "tab-sensitivity": "📐 Modellvergleich",
    "tab-por": "📊 POR-Analyse"
    }
    
    return [
        html.Div(
            tab_labels.get(tab_id, tab_id),
            id={"type":"suggestion", "tab": tab_id},
            className="search-suggestion-item",
            n_clicks=0
        )
        for _, tab_id in suggestions
    ]

@app.callback(
    Output("main-tabs", "value"),
    Input({"type": "suggestion", "tab": ALL}, "n_clicks"),
    prevent_initial_call=True
)
def switch_tab_by_click(n_clicks_list):
    # Zugriff auf den aktuellen Callback-Kontext
    # Der speichert, was genau das Callback ausgelöst hat
    ctx = callback_context

    # Wenn nichts den Callback ausgelöst hat, tue nichts
    if not ctx.triggered:
        return dash.no_update

    # Falls keine der Vorschlags-Komponenten überhaupt angeklickt wurde (alles 0 oder None), tue auch nichts
    if all(n in [0, None] for n in n_clicks_list):
        return dash.no_update

    # Die ID des Elements, das den Callback ausgelöst hat, extrahieren
    # Beispiel: '{"type":"suggestion","tab":"tab-core"}.n_clicks' → wir trennen am Punkt
    clicked_id_str = ctx.triggered[0]["prop_id"].split(".")[0]

    # Die ID zurück in ein Dictionary umwandeln → eval ist hier okay, da ID von dir kontrolliert
    clicked_id_dict = eval(clicked_id_str)

    # Gib den Tab-Wert zurück, damit das entsprechende Tab aktiviert wird
    return clicked_id_dict["tab"]
    


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8051))
    app.run(debug=True, host="0.0.0.0", port=port)













