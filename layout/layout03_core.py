from dash import dcc, html
from data.config import DATAFRAMES
from utils.plot_utils.core import plot_aep_comparison
from utils.compute_stats import get_aep_stats

# ------------------------------------------------------
# Layout: Zentrale Ergebnisse (AEP-Vergleich & Analyse)
# ------------------------------------------------------

core_layout = html.Div([

    # --- Titel ---
    html.H2([
        html.I(className="fas fa-chart-line", style={"marginRight": "10px"}),
        "Zentrale Ergebnisse"
    ], className="home-title"),

    # --- AEP-Vergleich ---
    html.H3("Monte-Carlo-basierte AEP-Vergleiche", className="home-subtitle"),

    html.P("""
        Die folgende Visualisierung zeigt zentrale Ergebnisse aus fünf Monte-Carlo-Simulationen 
        mit jeweils 2.000 Iterationen: ERA5, MERRA-2, deren Huber-gefilterte Varianten 
        sowie eine kombinierte Analyse beider Datensätze.
    """, className="home-paragraph"),

    html.P("""
        Für jede Simulation werden der durchschnittliche AEP-Wert (Mittelwert) sowie die 
        Unsicherheit (Variationskoeffizient) dargestellt. Ergänzend zeigen Boxplots, Jitterplots 
        und Violinplots die Verteilung der Simulationsergebnisse – inklusive Streuung und Ausreißern. 
        So lässt sich die Sensitivität der Ergebnisse in Abhängigkeit von Datensatz und Filtereinsatz 
        nachvollziehen.
    """, className="home-paragraph mb-40"),

    html.Div([
        dcc.Graph(
            id="aep-barplot",
            figure=plot_aep_comparison(get_aep_stats(DATAFRAMES), DATAFRAMES)
        )
    ], className="plot-container"),

    # --- Iterative Analyse ---
    html.H3("Iterationsspezifische Analyse", className="home-subtitle mt-40"),

    html.P("Für jede gewählte Simulation werden folgende Darstellungen gezeigt:", className="home-paragraph"),

    html.Ul([
        html.Li("Histogramm der AEP-Verteilung über alle Iterationen"),
        html.Li("Scatterplot zur Beziehung zwischen AEP und IAV-Faktor"),
        html.Li("Zeitlicher Verlauf der Simulation mit gleitendem Mittelwert (Fenstergröße: 50)")
    ], style={
        "marginLeft": "20px",
        "marginBottom": "15px",
        "lineHeight": "1.6",
        "fontSize": "16px"
    }),

    html.P("""
        Mehrere Simulationen können gleichzeitig ausgewählt und im Vergleich dargestellt werden.
    """, className="home-paragraph mb-40"),

    html.Div([
        dcc.Dropdown(
            id="mc-dropdown",
            options=[
                {"label": "ERA5", "value": "ERA5"},
                {"label": "MERRA2", "value": "MERRA2"},
                {"label": "Kombiniert", "value": "Kombiniert"},
                {"label": "ERA5 gefiltert", "value": "ERA5 gefiltert"},
                {"label": "MERRA2 gefiltert", "value": "MERRA2 gefiltert"},
            ],
            value=["ERA5"],
            clearable=False,
            multi=True,
            className="plot-dropdown-container"
        ),

        html.Div([
            dcc.Loading(
                id="aep-analysis-loading",
                type="circle",
                fullscreen=False,
                children=dcc.Graph(id="aep-analysis-plot")
            )
        ], className="plot-container")
    ])
], className="main-content")