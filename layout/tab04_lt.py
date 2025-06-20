from dash import dcc, html

tab_lt_layout = html.Div([
    html.H2("📉 Langzeitanalyse"),
    html.H3("Entwicklung der LT-Energie und IAV"),
    # Container für Dropdowns mit horizontaler Anordnung (50:50)
    html.Div([
        html.Div([
            html.Label("Monte-Carlo-Analysen auswählen:"),
            dcc.Dropdown(
                id="lt-mc-dropdown",
                options=[
                    {"label": "ERA5", "value": "ERA5"},
                    {"label": "MERRA2", "value": "MERRA2"},
                    {"label": "Kombiniert", "value": "Kombiniert"},
                    {"label": "ERA5 gefiltert", "value": "ERA5 gefiltert"},
                    {"label": "MERRA2 gefiltert", "value": "MERRA2 gefiltert"},
                ],
                value=["ERA5", "MERRA2"],
                clearable=False,
                multi=True,               
            )
        ], style={"flex": "1"}),

        html.Div([
            html.Label("LT-Variable auswählen:"),
            dcc.Dropdown(
                id="lt-metric-dropdown",
                options=[
                    {"label": "LT-Bruttoenergie", "value": "energy"},
                    {"label": "LT-Wind", "value": "wind"},
                ],
                value="energy",
                clearable=False
            )
        ], style={"flex": "1"})
    ], style={"display": "flex", "gap": "20px", "padding": "0 20px"}),

    html.Div([
        dcc.Loading(
            id="lt-loading",
            type="circle",
            fullscreen=False,
            children=dcc.Graph(id="lt-evolution-plot")
        )
    ], className="plot-container"),
    
    html.H3("LT-Energie vs Regressionssteigung"),
    
    html.Div([
        html.Label("Jahr(e) auswählen:"),
        dcc.Dropdown(
            id="lt-years-dropdown",
            options=[{"label": str(year), "value": year} for year in range (1,21)],
            value=[3, 6, 18],
            clearable=False,
            multi=True
        )     
    ], style={"marginBottom": "20px"}),
    
    html.Div([
        html.Div([
            html.Label("Linke MC-Analyse auswählen:"),
            dcc.Dropdown(
                id="lt-left-dropdown",
                options=[
                    {"label": "ERA5", "value": "ERA5"},
                    {"label": "MERRA2", "value": "MERRA2"},
                    {"label": "Kombiniert", "value": "Kombiniert"},
                    {"label": "ERA5 gefiltert", "value": "ERA5 gefiltert"},
                    {"label": "MERRA2 gefiltert", "value": "MERRA2 gefiltert"},
                ],
                value="ERA5",
                clearable=False
            )           
        ], style={"flex":"1"}),
        
        html.Div([
            html.Label("Rechte MC-Analyse auswählen:"),
            dcc.Dropdown(
                id="lt-right-dropdown",
                options=[
                    {"label": "ERA5", "value": "ERA5"},
                    {"label": "MERRA2", "value": "MERRA2"},
                    {"label": "Kombiniert", "value": "Kombiniert"},
                    {"label": "ERA5 gefiltert", "value": "ERA5 gefiltert"},
                    {"label": "MERRA2 gefiltert", "value": "MERRA2 gefiltert"},
                ],
                value="MERRA2",
                clearable=False
            )
        ], style={"flex":"1"})
    ], style={"display":"flex", "gap":"20px"}),
    
    html.Div([
        dcc.Loading(
            id="lt-slope-loading",
            type="circle",
            fullscreen=False,
            children=dcc.Graph(id="lt-slope-plot")
        )
    ], className="plot-container")
], className="content-wrapper")
















