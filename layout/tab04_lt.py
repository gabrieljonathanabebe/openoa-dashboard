from dash import dcc, html

tab_lt_layout = html.Div([
    # Titel mit Icon
    html.H2([
        html.I(className="fas fa-wave-square", style={"marginRight": "10px"}),
        "Langzeitanalyse"
    ], className="home-title"),

    # Einführungstext zur LT-Analyse
    html.P("""
        Diese Ansicht untersucht die langfristige Korrektur des Energieertrags innerhalb jeder Monte-Carlo-Analyse. 
        Der Fokus liegt auf der interannuellen Variabilität (IAV), welche als Haupttreiber für die Unsicherheit in der 
        AEP-Prognose gilt.
    """, className="home-paragraph"),

    # Untertitel & Beschreibung zur ersten Grafik
    html.H3("Entwicklung der Energie und IAV", className="home-subtitle"),
    html.P("""
        Die linke Grafik zeigt die jährliche Bruttoenergie eines Windparks über die Langzeitperiode. 
        Die gestrichelte Linie stellt den modellierten Jahreswert dar, während die durchgezogene Linie 
        den kumulierten Mittelwert zeigt und damit visualisiert, wie sich die Prognose mit zunehmender Zeit stabilisiert.
    """, className="home-paragraph"),
    html.P("""
        Auf der rechten Seite wird die Entwicklung der interannuellen Variabilität (IAV) dargestellt. 
        Über Dropdown-Menüs lassen sich verschiedene Monte-Carlo-Analysen auswählen sowie optional 
        zwischen Energie- und Winddaten umschalten.
    """, className="home-paragraph"),

    # Dropdowns (Seite an Seite)
    html.Div([
        html.Div([
            html.Label("Monte-Carlo-Analysen auswählen:", className="home-paragraph"),
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
            html.Label("LT-Variable auswählen:", className="home-paragraph"),
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

    # Plot: Entwicklung
    html.Div([
        dcc.Loading(
            id="lt-loading",
            type="circle",
            fullscreen=False,
            children=dcc.Graph(id="lt-evolution-plot")
        )
    ], className="plot-container"),

    # Untertitel & Erklärung zum zweiten Plot
    html.H3("Energie vs. Regressionssteigung", className="home-subtitle"),
    html.P([
        """In diesem Scatterplot-Vergleich können zwei Monte-Carlo-Analysen visuell gegenübergestellt werden.
        Die y-Achse zeigt die vorhergesagte jährliche Energie, die x-Achse die berechnete Regressionssteigung.
        Die Farbskala kodiert die durchschnittliche Windgeschwindigkeit im jeweiligen Jahr."""
    ], className="home-paragraph"),
    html.P("Über das Dropdown-Feld lassen sich bestimmte Jahre gezielt auswählen.", className="home-paragraph"),

    # Dropdown zur Auswahl der Jahre
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

    # Vergleich zweier MC-Simulationen
    html.Div([
        html.Div([
            html.Label("Linke MC-Analyse auswählen:", className="home-paragraph"),
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
            html.Label("Rechte MC-Analyse auswählen:", className="home-paragraph"),
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

    # Plot: Slope-Energy
    html.Div([
        dcc.Loading(
            id="lt-slope-loading",
            type="circle",
            fullscreen=False,
            children=dcc.Graph(id="lt-slope-plot")
        )
    ], className="plot-container")
], className="main-content")