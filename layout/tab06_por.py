from dash import dcc, html
from data.config import DATAFRAMES, POR_DATAFRAMES

tab_por_layout = html.Div([

    html.H2([
        html.I(className="fas fa-chart-area", style={"marginRight": "10px"}),
        "Analyse der POR-Modellierung"
    ], className="home-title"),

    html.Div([
    
        # Oberer Textabschnitt
        html.Div([
            html.P("""
                In dieser Analyse wird untersucht, wie präzise die modellierte Jahresenergie (GPS) 
                der Period of Record (POR) über alle Iterationen hinweg berechnet wurde – unabhängig 
                von der Modellgüte der Bootstrapping-Stichprobe. Die POR-Modellierung basiert auf der 
                Anwendung des trainierten Modells auf die Gesamtheit der Daten (nicht nur das Trainingssample) 
                und bietet somit einen direkten Einblick in die realitätsnahe Prognosekraft der MC-Analysen.
            """, className="home-paragraph"),
    
            html.H3("Verteilung der modellierten Jahresenergie (GPS)", className="home-subtitle"),
    
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
            """, className="home-paragraph")
        ], className="section-text-block"),  # du kannst hier marginBottom per CSS definieren
    
        # Plot + Dropdowns nebeneinander
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
    
                html.Label("Optionen:"),
                dcc.Checklist(
                    id="por-options",
                    options=[
                        {"label": "Beobachteter Wert", "value": "show-observed"},
                        {"label": "Mittelwerte der MC-Analysen", "value": "show-means"},
                    ],
                    value=[],
                    labelStyle={"display": "block", "marginBottom": "0px", "fontSize": "15px", "marginTop": "10px"}
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
            "alignItems": "center",
        })   
    ]),
    
    html.Div([        
        html.Div([                            
            html.H3("Regressionsbasierte Modellanalyse nach Iteration", className="home-subtitle"),
        
            html.P("""
                Dieser Abschnitt erlaubt eine gezielte Untersuchung einzelner Modelliterationsergebnisse auf Basis verschiedener 
                Regressionsmetriken. Für zwei ausgewählte MC-Analysen wird jeweils diejenige Iteration herausgefiltert, 
                die – je nach Auswahl – beispielsweise den höchsten oder niedrigsten Regressionskoeffizienten (Slope) aufweist.
            """, className="home-paragraph"),
            
            html.P("""
                Die beiden Diagramme stellen jeweils die zugrundeliegenden Bootstrapping- (grün) und Non-Bootstrapping-Datenpunkte (rot) 
                dar. Die gestrichelte Regressionslinie beschreibt das zugrundeliegende lineare Modell der jeweiligen Iteration. 
                Über den Diagrammen werden ergänzende Metriken angezeigt, darunter das Bestimmtheitsmaß R², der mittlere quadratische Fehler (MSE) 
                sowie der geschätzte jährliche Modellbias.
            """, className="home-paragraph"),
            
        ], className="section-text-block"),
                   
        html.Div([
            
            html.Div([
                html.Label("Metrik:", className="home-paragraph"),
                dcc.Dropdown(
                    id="por-metric-dropdown", 
                    options=[
                        {"label":"Slope (GWh/(m/s))", "value":"slope"},
                        {"label":"Intercept (GWh)", "value":"intercept"},
                        {"label":"R Squared (R²)", "value":"r2"},
                        {"label":"Mean Squared Error (MSE)", "value":"mse"},
                        {"label":"Bias (GWh/yr)", "value":"yearly_bias"}
                    ],
                    value="slope",
                    clearable=False
                ),
                html.Label("Wert:", className="home-paragraph"),
                dcc.Dropdown(
                    id="por-metric-value-dropdown", 
                    options=[
                        {"label": "Maximum", "value": "max"},
                        {"label": "3. Quantil", "value": "q3"},
                        {"label": "Median", "value": "median"},
                        {"label": "1. Quantil", "value": "q1"},
                        {"label": "Minimum", "value": "min"},
                    ],
                    value="max",
                    clearable=False
                )
            ], style={"flex": "1"}, className="sidebar-dropdown-group"),
            
            html.Div([
                html.Div([
                    html.Div([
                        html.Label("MC-Analyse links:", className="home-paragraph"),
                        dcc.Dropdown(
                            id="reg-scatter-label-dropdown-1",
                            options=[
                                {"label": label, "value": label} for label in POR_DATAFRAMES.keys()
                            ],
                            value="ERA5",
                            clearable=False
                        )
                    ], style = {"flex":"1"}),
                    html.Div([
                        html.Label("MC-Analyse rechts:", className="home-paragraph"),
                        dcc.Dropdown(
                            id="reg-scatter-label-dropdown-2",
                            options=[
                                {"label": label, "value": label} for label in POR_DATAFRAMES.keys()
                            ],
                            value="MERRA2",
                            clearable=False
                        )
                    ], style = {"flex":"1"}),
                ], style={"display": "flex"}, className="plot-dropdown-container"),
            
                html.Div([
                    dcc.Loading(
                        id="reg-scatter-loading",
                        type="circle",
                        fullscreen=False,
                        children=dcc.Graph(id="reg-scatter")
                    )
                ], className="plot-container")       
            ], style={"flex":"7"})
        ], className="centered-flex-row"),
        
        html.Div([              
            html.P("""
                Auf diese Weise lässt sich nachvollziehen, wie stark die Regressionsparameter innerhalb einzelner Iterationen schwanken 
                und welche Datenpunkte maßgeblich zum Modellverhalten beitragen. Die Visualisierung unterstützt insbesondere beim 
                Vergleich unterschiedlicher Reanalyseprodukte oder beim Erkennen systematischer Abweichungen zwischen Trainings- 
                und Testdaten.
            """, className="home-paragraph"),
        ], className="section-text-block")
     ]),
        

], className="main-content")
        
        
        
        
        
        
        
        
        
        
        
        
        
        