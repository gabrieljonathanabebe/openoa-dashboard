from dash import dcc, html
from data.config import DATAFRAMES
from utils.plot_utils import get_aep_compare_plots
from utils.compute_stats import get_aep_stats

tab_core_layout = html.Div([
    html.H2([
        html.I(className="fas fa-chart-line", style={"marginRight": "10px"}),
        "Zentrale Ergebnisse"
    ], className="home-title"),

    html.H3("Monte-Carlo-basierte AEP-Vergleiche", className="home-subtitle"),
    html.P("""
        Die nachfolgende Visualisierung zeigt zentrale Resultate aus fünf Monte-Carlo-Simulationen 
        mit je 2000 Iterationen: ERA5, MERRA-2, die jeweils Huber-gefilterten Varianten sowie 
        eine kombinierte Analyse. 
    """, className="home-paragraph"),
    html.P("""
        Dargestellt sind für jede Analyse sowohl der mittlere AEP-Wert (Mittelwert über alle Iterationen) 
        als auch die Unsicherheit (Variationskoeffizient). Ergänzend geben Boxplots, Jitterplots 
        und Violinplots Einblick in die Verteilung der AEP-Prognosen – inklusive Ausreißer und Streuung. 
        So lässt sich die Sensitivität der AEP-Ergebnisse gegenüber Datengrundlage und Filtereinsatz 
        anschaulich bewerten.
    """, className="home-paragraph mb-40"),

    html.Div([
        dcc.Graph(
            id="aep-barplot",
            figure=get_aep_compare_plots(get_aep_stats(DATAFRAMES), DATAFRAMES)
        )
    ], className="plot-container"),

    html.H3("Iterationsspezifische Analyse", className="home-subtitle mt-40"),
    html.P("Die folgende Analyse zeigt für jede ausgewählte MC-Simulation:", className="home-paragraph"),
    html.Ul([
        html.Li("Die Verteilung der AEP über alle Iterationen (Histogramm)"),
        html.Li("Die Beziehung zwischen AEP und dem gesampelten IAV-Faktor (Scatter)"),
        html.Li("Den iterativen Verlauf der Prognose mit gleitendem Mittelwert (Linienplot, Fenstergröße 50)")
    ], style={"marginLeft": "20px", "marginBottom": "15px", "lineHeight": "1.6", "fontSize": "16px"}),
    
    html.P("Durch Auswahl mehrerer Analysen im Dropdown können diese direkt überlagert und visuell verglichen werden.", className="home-paragraph mb-40"),

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