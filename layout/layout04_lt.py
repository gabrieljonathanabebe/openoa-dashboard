from dash import dcc, html

# ------------------------------------------------------
# Layout: Langzeitanalyse
# ------------------------------------------------------

lt_layout = html.Div([
    # Titel mit Icon
    html.H2([
        html.I(className="fas fa-wave-square", style={"marginRight": "10px"}),
        "Langzeitanalyse"
    ], className="home-title"),

    # Einführung
    html.P("""
        In dieser Ansicht wird die langfristige Entwicklung des Energieertrags in den verschiedenen 
        Monte-Carlo-Analysen untersucht. Im Mittelpunkt steht die interannuelle Variabilität (IAV), 
        die als wesentliche Quelle für Unsicherheiten in der AEP-Prognose gilt.
    """, className="home-paragraph"),

    # Untertitel & Beschreibung zur ersten Visualisierung
    html.H3("Entwicklung von Energie und IAV", className="home-subtitle"),
    html.P("""
        Die linke Visualisierung zeigt die jährliche Bruttoenergie eines Windparks über die Langzeitperiode. 
        Die transparenten Linien bilden die jährlichen Modellwerte ab, während die kräftigeren Linien den 
        kumulierten Mittelwert darstellt. Sie verdeutlicht, wie sich die Prognose über die Zeit stabilisiert.
    """, className="home-paragraph"),
    html.P("""
        Rechts daneben ist die Entwicklung der interannuellen Variabilität (IAV) zu sehen. Über die Dropdown-Menüs 
        lassen sich verschiedene Monte-Carlo-Analysen einblenden oder zwischen Energie- und Winddaten umschalten.
    """, className="home-paragraph mb-40"),

    # Dropdowns zur Steuerung
    html.Div([
        html.Div([
            html.Label("MC-Analysen auswählen:", className="home-paragraph"),
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
            html.Label("LT-Variable:", className="home-paragraph"),
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
    ], style={"display": "flex"}, className="plot-dropdown-container"),

    # Plot zur Langzeitentwicklung
    html.Div([
        dcc.Loading(
            id="lt-loading",
            type="circle",
            fullscreen=False,
            children=dcc.Graph(id="lt-evolution-plot")
        )
    ], className="plot-container"),

    # Zweiter Abschnitt: Slope-Analyse
    html.H3("Energie im Verhältnis zur Regressionssteigung", className="home-subtitle mt-40"),
    html.P("""
        Dieser Scatterplot-Vergleich stellt zwei Monte-Carlo-Analysen gegenüber. Auf der y-Achse ist die prognostizierte 
        Jahresenergie zu sehen, auf der x-Achse die berechnete Regressionssteigung. Die Farbskala zeigt zusätzlich 
        die durchschnittliche Windgeschwindigkeit pro Jahr.
    """, className="home-paragraph"),
    html.P("Die Auswahl spezifischer Jahre erfolgt über das Dropdown-Feld unten.", className="home-paragraph mb-40"),

    # Dropdown: Jahre
    html.Div([
        html.Label("Jahr(e) auswählen:", className="home-paragraph"),
        dcc.Dropdown(
            id="lt-years-dropdown",
            options=[{"label": str(year), "value": year} for year in range(1, 21)],
            value=[3, 6, 18],
            clearable=False,
            multi=True
        )
    ], style={"marginBottom": "20px"}, className="plot-dropdown-container"),

    # Vergleich zweier Analysen
    html.Div([
        html.Div([
            html.Label("Linke Analyse:", className="home-paragraph"),
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
        ], style={"flex": "1"}),

        html.Div([
            html.Label("Rechte Analyse:", className="home-paragraph"),
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
        ], style={"flex": "1"})
    ], style={"display": "flex"}, className="plot-dropdown-container"),

    # Plot zur Slope-Energie-Korrelation
    html.Div([
        dcc.Loading(
            id="lt-slope-loading",
            type="circle",
            fullscreen=False,
            children=dcc.Graph(id="lt-slope-plot")
        )
    ], className="plot-container")
], className="main-content")