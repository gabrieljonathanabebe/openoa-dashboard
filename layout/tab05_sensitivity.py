from dash import dcc, html
from data.config import DATAFRAMES, METRIC_INFO

tab_sensitivity_layout = html.Div([
    
    html.H2("📐 Prognosegüte & Modellvergleich"),
    html.H3("Verteilung der Modellkoeffizienten"),
    
    html.Div([
        
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
                value="slope",
                clearable=False
            ),
            
            html.Br(),
            
            html.Label("MC-Analyse 1 auswählen:"),
            dcc.Dropdown(
                id="label-1-dropdown",
                options=[
                    {"label":label, "value":label} for label in DATAFRAMES.keys()
                ],
                value="ERA5",
                clearable=False,            
            ),
            
            html.Br(),
            
            html.Label("MC-Analyse 2 auswählen:"),
            dcc.Dropdown(
                id="label-2-dropdown",
                options=[
                    {"label":label, "value":label} for label in DATAFRAMES.keys()
                ],
                value="ERA5 gefiltert",
                clearable=False,            
            ),
        ], style={"flex": "1", "marginTop":"80px"}),
        
        html.Div([
            dcc.Loading(
                id="model-comparison-plot-loading",
                type="circle",
                fullscreen=False,
                children=dcc.Graph(id="model-comparison-plot")
            )
        ], style={"flex": "5"}, className="plot-container")
    ], style={"display":"flex", "gap":"20px"}),
    
    html.H3("Sensitivität gegenüber Modellkoeffizienten"),
    
    html.Div([
        html.Div([
            
            html.Label("X-Achse auswählen:"),
            dcc.Dropdown(
                id="x-metric-dropdown",
                options=[
                    {"label": info["metric_en"], "value": key} for key, info in METRIC_INFO.items()
                ],
                value="intercept",
                clearable=False
            ),
            
            html.Br(),
            
            html.Label("Y-Achse auswählen:"),
            dcc.Dropdown(
                id="y-metric-dropdown",
                options=[
                    {"label": info["metric_en"], "value": key} for key, info in METRIC_INFO.items()
                ],
                value="slope",
                clearable=False
            ),
            
            html.Br(),
            
            html.Label("Farbmetrik (z) auswählen:"),
            dcc.Dropdown(
                id="z-metric-dropdown",
                options=[
                    {"label": info["metric_en"], "value": key} for key, info in METRIC_INFO.items()
                ],
                value="r2",
                clearable=False
            )
            
        ], style={"flex": "1", "marginTop":"60px"}),
        
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
            ], style={"display": "flex", "gap": "20px"}),

            
            html.Div([
                dcc.Loading(
                    id="model-scatter-loading",
                    type="circle",
                    fullscreen=False,
                    children=dcc.Graph(id="modell-scatterplot")
                )                
            ], className="plot-container")
        ], style={"flex": "5"})
    ], style={"display":"flex", "gap":"20px"}),
    
    html.H3("Korrelationsmatrix der Modellmetriken"),
    
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
    ], style={"display": "flex", "gap": "20px"}),
    
    html.Br(),
    
    html.Div([
        dcc.Loading(
            type="circle",
            children=dcc.Graph(id="correlation-matrix"),
        )
    ], className="plot-container")
])




























