from dash import dcc, html
from data.config import DATAFRAMES, METRIC_INFO

tab_sensitivity_layout = html.Div([
    

    # Titel mit passendem Icon (Regression/Analyse)
    html.H2([
        html.I(className="fas fa-chart-line", style={"marginRight": "10px"}),
        "Einfluss der Regressionsparameter"
    ], className="home-title"),

    # Einleitungstext
    html.P("""
        In diesem Abschnitt wird untersucht, wie sich Regressionsparameter wie Steigung, Achsenabschnitt, R² und MSE auf die 
        AEP-Prognose auswirken und welche Unterschiede zwischen den Monte-Carlo-Analysen bestehen. 
        Im Fokus steht insbesondere der Einfluss der Huber-Regression auf die Modellgüte und die Robustheit 
        der POR-Modellierung.
    """, className="home-paragraph"),

    html.H3("Verteilung der Modellkoeffizienten", className="home-subtitle"),

    html.P("""
        Wähle oben gezielt einen Regressionsparameter aus – etwa die Steigung oder das Bestimmtheitsmaß R² – 
        und vergleiche anschließend zwei Monte-Carlo-Analysen miteinander. Die Histogramm-Darstellung links zeigt die Verteilung, 
        während der asymmetrische Violinplot rechts zusätzlich die Dichteverteilung und Einzelsimulationen visualisiert.
    """, className="home-paragraph mb-40"),

    # Dropdowns und Grafik
    html.Div([

        # Steuerungsbereich
        html.Div([
            html.Label("Koeffizient auswählen:"),
            dcc.Dropdown(
                id="metric-dropdown",
                options=[
                    {"label":"Steigung (GWh/(m/s))", "value":"slope"},
                    {"label":"Achsenabschnitt (GWh)", "value":"intercept"},
                    {"label":"Bestimmtheitsmaß (R²)", "value":"r2"},
                    {"label":"Mean Squared Error (MSE)", "value":"mse"}
                ],
                value="r2",
                clearable=False
            ),

            html.Br(),

            html.Label("MC-Analyse 1 auswählen:"),
            dcc.Dropdown(
                id="label-1-dropdown",
                options=[{"label": label, "value": label} for label in DATAFRAMES.keys()],
                value="ERA5",
                clearable=False,
            ),

            html.Br(),

            html.Label("MC-Analyse 2 auswählen:"),
            dcc.Dropdown(
                id="label-2-dropdown",
                options=[{"label": label, "value": label} for label in DATAFRAMES.keys()],
                value="MERRA2",
                clearable=False,
            ),
        ], style={"flex": "1"}, className="sidebar-dropdown-group"),

        # Grafikbereich
        html.Div([
            dcc.Loading(
                id="model-comparison-plot-loading",
                type="circle",
                fullscreen=False,
                children=dcc.Graph(id="model-comparison-plot")
            )
        ], style={"flex": "5"}, className="plot-container")
    ], className="centered-flex-row"),
    
    html.H3("Beziehungen der Modellparameter", className="home-subtitle mt-40"),

    html.P("""
        In dieser interaktiven Analyse lassen sich je zwei Modellparameter auf der X- und Y-Achse vergleichen. 
        Über die Farbkodierung wird eine zusätzliche Kennzahl eingebunden – etwa R², die AEP oder IAV –, um dreidimensionale 
        Zusammenhänge visuell zu erfassen. Dadurch können Einflussfaktoren identifiziert werden, die signifikant zur 
        Streuung der Modellgüte beitragen.
    """, className="home-paragraph"),
    
    html.P("""
        Besonders spannend ist der Vergleich zwischen zwei MC-Analysen: So lässt sich untersuchen, ob sich Regressionsparameter 
        (z. B. Steigung oder Achsenabschnitt) systematisch auf Langzeitkennzahlen auswirken – oder ob bestimmte Filter (etwa die 
        Huber-Regression) strukturelle Unterschiede im Modellverhalten erzeugen.
    """, className="home-paragraph mb-40"),
    
    html.Div([
        html.Div([
            
            html.Label("X-Achse auswählen:"),
            dcc.Dropdown(
                id="x-metric-dropdown",
                options=[
                    {"label": info["metric_en"], "value": key} for key, info in METRIC_INFO.items()
                ],
                value="mse",
                clearable=False
            ),
            
            html.Br(),
            
            html.Label("Y-Achse auswählen:"),
            dcc.Dropdown(
                id="y-metric-dropdown",
                options=[
                    {"label": info["metric_en"], "value": key} for key, info in METRIC_INFO.items()
                ],
                value="r2",
                clearable=False
            ),
            
            html.Br(),
            
            html.Label("Farbmetrik (z) auswählen:"),
            dcc.Dropdown(
                id="z-metric-dropdown",
                options=[
                    {"label": info["metric_en"], "value": key} for key, info in METRIC_INFO.items()
                ],
                value="slope",
                clearable=False
            )
            
        ], style={"flex": "1"}, className="sidebar-dropdown-group"),
        
        html.Div([
            html.Div([
                html.Div([
                    html.Label("MC-Analyse (links):"),
                    dcc.Dropdown(
                        id="scatter-label-1-dropdown",
                        options=[
                            {"label":label, "value":label} for label in DATAFRAMES.keys()
                        ],
                        value="ERA5",
                        clearable=False
                    )               
                ], style={"flex": "1"}),
                
                html.Div([
                    html.Label("MC-Analyse (rechts):"),
                    dcc.Dropdown(
                        id="scatter-label-2-dropdown",
                        options=[
                            {"label":label, "value":label} for label in DATAFRAMES.keys()
                        ],
                        value="MERRA2",
                        clearable=False
                    ),                
                ], style={"flex": "1"}),                
            ], style={"display": "flex"}, className="plot-dropdown-container"),

            
            html.Div([
                dcc.Loading(
                    id="model-scatter-loading",
                    type="circle",
                    fullscreen=False,
                    children=dcc.Graph(id="modell-scatterplot")
                )                
            ], className="plot-container")
        ], style={"flex": "5"})
    ], className="centered-flex-row"),
    
    html.H3("Korrelationsmatrix der Modellmetriken", className="home-subtitle mt-40"),

    html.P("""
        Die nachfolgenden Heatmaps zeigen kompakt, wie stark verschiedene Modellmetriken miteinander korrelieren. 
        Beispielsweise kann überprüft werden, ob ein hohes Bestimmtheitsmaß mit einer geringen Prognoseunsicherheit 
        oder einem bestimmten AEP-Wert einhergeht.
    """, className="home-paragraph"),
    
    html.P("""
        Ein direkter Vergleich zweier Monte-Carlo-Analysen erlaubt Rückschlüsse darauf, ob sich bestimmte Zusammenhänge 
        (z. B. zwischen IAV und Regressionssteigung) nur auf spezifische Datensätze beschränken – oder systematisch in 
        allen Simulationen auftreten.
    """, className="home-paragraph mb-40"),
    
    html.Div([
        html.Div([
            html.Label("MC-Analyse (links):"),
            dcc.Dropdown(
                id="corr-left-label-dropdown",
                options=[{"label": label, "value": label} for label in DATAFRAMES.keys()],
                value="ERA5"
            ),
        ], style={"flex": "1"}),
    
        html.Div([
            html.Label("MC-Analyse (rechts):"),
            dcc.Dropdown(
                id="corr-right-label-dropdown",
                options=[{"label": label, "value": label} for label in DATAFRAMES.keys()],
                value="MERRA2"
            ),
        ], style={"flex": "1"}),
    ], style={"display": "flex"}, className="plot-dropdown-container"),
    
    html.Div([
        dcc.Loading(
            type="circle",
            children=dcc.Graph(id="correlation-matrix"),
        )
    ], className="plot-container")
], className="main-content")


























