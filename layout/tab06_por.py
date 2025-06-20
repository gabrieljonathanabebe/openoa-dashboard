from dash import dcc, html
from data.config import DATAFRAMES

tab_por_layout = html.Div([

    html.H2("📊 POR-Analyse"),
    
    html.H3("Verteilung der modellierten jährlichen Energie (GPS)"),

    html.Div([
        
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
            html.Br(),
            
            dcc.Checklist(
                id="por-options",
                options=[
                    {"label": "Beobachteter Wert", "value": "show-observed"},
                    {"label": "Mittelwerte der MC-Analysen", "value": "show-means"},
                ],
                value=[],
                labelStyle={"display": "block", "marginBottom": "5px", "fontSize": "15px", "marginTop": "10px"}
            ),
            
        ], style={
            "flex": "1",
            "minWidth": "200px"
        }),
    
        # Rechte Spalte mit Plot
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
], className="content-wrapper")