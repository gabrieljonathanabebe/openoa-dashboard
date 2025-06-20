from dash import html


tab_home_layout = html.Div([
    html.Div([  # Innerer Wrapper für bessere Lesbarkeit
        html.H2([
            html.I(className="fas fa-chart-bar", style={"marginRight": "10px"}),
            "Windpark-Ertragsanalyse mit Reanalyse-Daten"
        ], className="home-title"),

        html.H4([
            html.I(className="fas fa-wind", style={"marginRight": "10px"}),
            "Projektüberblick"
        ], className="home-subtitle"),
        html.P("""
            Diese interaktive Anwendung wurde im Rahmen einer Bachelorarbeit entwickelt und visualisiert die
            Auswirkungen verschiedener Reanalyse-Produkte (ERA5, MERRA-2, kombiniert) auf die Langzeitprognose
            der Energieproduktion eines Windparks.
        """, className="home-paragraph"),

        html.P("""
            Mithilfe des OpenOA-Frameworks wurden die Daten analysiert und aufbereitet, um Unsicherheiten und
            Modellunterschiede nachvollziehbar darzustellen.
        """, className="home-paragraph"),

        html.H4([
            html.I(className="fas fa-search", style={"marginRight": "10px"}),
            "Methodischer Fokus"
        ], className="home-subtitle"),
        html.P("""
            Die Analyse umfasst die Korrektur historischer Energieerträge, Anwendung eines robusten Huber-Filters
            sowie die Kombination von Reanalyse-Datensätzen zur optimierten Unsicherheitsbewertung.
        """, className="home-paragraph"),
        html.P("""
            Besonderes Augenmerk liegt auf der interannuellen Variabilität und der robusten Schätzung
            des Annual Energy Production (AEP).
        """, className="home-paragraph"),

        html.H4([
            html.I(className="fas fa-compass", style={"marginRight": "10px"}),
            "Navigation"
        ], className="home-subtitle"),
        html.P("""
            Nutzen Sie die Navigation auf der linken Seite, um zentrale Kennzahlen, Scatterplots sowie
            die Langzeitanalyse interaktiv zu erkunden.
        """, className="home-paragraph"),

        html.Hr(),

        html.H4([
            html.I(className="fas fa-envelope", style={"marginRight": "10px"}),
            "Kontakt"
        ], className="home-subtitle"),
        html.P("Gabriel Jonathan Abebe", className="home-paragraph"),
        html.P("jonathan.abebe@hs-ansbach.de", className="home-paragraph"),
        html.P("Bachelorarbeit – 2025, Hochschule Ansbach", className="home-paragraph"),

        html.H4([
            html.I(className="fas fa-tools", style={"marginRight": "10px"}),
            "Technologien"
        ], className="home-subtitle"),
        html.P("Erstellt mit Dash (Plotly), Pandas, Plotly Graph Objects und OpenOA.", className="home-paragraph"),
        html.P("Version 1.0 – Stand: Juni 2025", className="home-paragraph"),

        # Optional: Logo
        # html.Img(src="/assets/unilogo.png", style={"width": "140px", "marginTop": "25px"})
    ], className="main-content")
])




