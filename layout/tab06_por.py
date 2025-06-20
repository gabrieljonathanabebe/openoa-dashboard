from dash import dcc, html
from data.config import DATAFRAMES

tab_por_layout = html.Div([
    
    html.H2([
        html.I(className="fas fa-chart-area", style={"marginRight": "10px"}),
        "Analyse der POR-Modellierung"
    ], className="home-title"),

    html.P("""
        In dieser Analyse wird untersucht, wie präzise die modellierte Jahresenergie (GPS) 
        der Period of Record (POR) über alle Iterationen hinweg berechnet wurde – unabhängig 
        von der Modellgüte der Bootstrapping-Stichprobe. Die POR-Modellierung basiert auf der 
        Anwendung des trainierten Modells auf die Gesamtheit der Daten (nicht nur das Trainingssample) 
        und bietet somit einen direkten Einblick in die realitätsnahe Prognosekraft der MC-Analysen.
    """, className="home-paragraph"),

    html.P("""
        Die Histogramm-Darstellung links zeigt die Verteilung der modellierten GPS-Werte für zwei ausgewählte Analysen. 
        Rechts lässt sich im asymmetrischen Violinplot zusätzlich die Dichteverteilung und die Streuung einzelner 
        Simulationen visuell erfassen. Auf diese Weise kann abgeschätzt werden, welche Analyse stabilere Vorhersagen 
        liefert und in welchem Maße die Prognosen über alle Iterationen hinweg schwanken.
    """, className="home-paragraph"),

    html.P("""
        Über die Checkboxen lassen sich zusätzliche Informationen einblenden: 
        Die tatsächliche, gemessene Energie der Windparkdaten im POR-Zeitraum (als gestrichelte Linie) sowie 
        die Mittelwerte der simulierten Verteilungen – um etwaige systematische Abweichungen und potenzielle 
        Modell-Biases frühzeitig sichtbar zu machen.
    """, className="home-paragraph"),

    html.H3("Verteilung der modellierten Jahresenergie (GPS)", className="home-subtitle"),

    html.Div([
            
        # Linke Steuerungsleiste
        html.Div([
            html.Label("MC-Analyse 1:"),
            dcc.Dropdown(
                id="por-label-1-dropdown",
                options=[{"label": label, "value": label} for label in DATAFRAMES.keys()],
                value="ERA5",
                clearable=False
            ),
            html.Br(),
        
            html.Label("MC-Analyse 2:"),
            dcc.Dropdown(
                id="por-label-2-dropdown",
                options=[{"label": label, "value": label} for label in DATAFRAMES.keys()],
                value="ERA5 gefiltert",
                clearable=False
            ),
            html.Br(),
        
            html.Label("Optionen:"),
            dcc.Checklist(
                id="por-options",
                options=[
                    {"label": "Beobachteter Wert", "value": "show-observed"},
                    {"label": "Mittelwerte der MC-Analysen", "value": "show-means"},
                ],
                value=[],
                labelStyle={"display": "block", "marginBottom": "5px", "fontSize": "15px", "marginTop": "10px"}
            )
        ], style={"flex": "1", "minWidth": "200px"}, className="centered-column-flex sidebar-dropdown-group"),


        # Rechte Seite: Plot
        html.Div([
            dcc.Loading(
                id="por-histogram-loading",
                type="circle",
                children=dcc.Graph(id="por-histogram-violin-plot")
            )
        ], style={"flex": "5"}, className="plot-container")

    ], style={
        "display": "flex",
        "gap": "20px",
        "alignItems": "flex-start",
        "marginBottom": "30px"
    })

], className="main-content")